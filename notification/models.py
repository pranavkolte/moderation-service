from django.db import models
from django.conf import settings
import uuid


class ViolationNotification(models.Model):
    notification_id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        db_index=True
    )
    post_id = models.ForeignKey(
        'post.Post',
        on_delete=models.CASCADE,
        related_name='notifications',
        db_index=True
    )
    comment_id = models.ForeignKey(
        'post.Comment',
        on_delete=models.CASCADE,
        related_name='notifications',
        db_index=True
    )
    
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notification'
        ordering = ['-created_at']