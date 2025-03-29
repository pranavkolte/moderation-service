from celery import shared_task
from django.utils import timezone
from django.db import transaction, models
from service import moderation_service
from .models import Comment
from user.models import UserViolation, User  # Add User import
from notification.models import ViolationNotification

VIOLATION_THRESHOLD = 0.7  # 70%
MAX_VIOLATIONS = 3  # Maximum violations before user deletion

@shared_task
def report_comment(comment_id, post_id, user_id):
    try:
        # get user
        try:
            user = User.objects.get(user_id=user_id)
        except (ValueError, User.DoesNotExist):
            # If user_id is not uuid then try usename
            user = User.objects.get(username=user_id)
            
        comment = Comment.objects.get(comment_id=comment_id)

        # Check if user has already reported this conmet
        existing_report = ViolationNotification.objects.filter(
            user=user,
            comment_id=comment
        ).exists()

        if existing_report:
            return False 

        moderation_result = moderation_service.moderate_text(comment.content)
        categories = moderation_result.get('moderationCategories', [])

        violating_categories = [
            (category['name'], category['confidence'])
            for category in categories
            if category.get('confidence', 0) >= VIOLATION_THRESHOLD
        ]

        if not violating_categories:
            return True

        with transaction.atomic():
            comment.is_flagged = True
            comment.flagged_at = timezone.now()
            comment.save()

            violation = UserViolation.objects.filter(user=user).first()
            if violation:
                violation.violation_count = models.F('violation_count') + 1
                violation.save()
            else:
                violation = UserViolation.objects.create(
                    user=user,
                    violation_count=1
                )
            violation.refresh_from_db()

            category_details = "\n".join(
                f"- {name}: {confidence:.2%}" 
                for name, confidence in violating_categories
            )
            highest_score = max(confidence for _, confidence in violating_categories)
            
            # Create notification
            ViolationNotification.objects.create(
                user=user,
                post_id_id=post_id,
                comment_id=comment,
                message=(
                    "Content policy violation detected:\n"
                    f"{category_details}\n"
                    f"Highest violation score: {highest_score:.2%}"
                )
            )

            if violation.violation_count >= MAX_VIOLATIONS:
                user.is_active = False
                user.save()
                
                ViolationNotification.objects.create(
                    user=user,
                    post_id_id=post_id,
                    comment_id=comment,
                    message="Account deactivated due to repeated violations"
                )
                
                comment.delete()

        return True

    except Exception as error:
        print(f"Error processing comment report: {str(error)}")
        if "prohibited to prevent data loss" in str(error):
            print("Failed to save notification due to invalid comment reference")
        return False
