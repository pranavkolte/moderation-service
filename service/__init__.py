from .moderation import ModerationService
from django.conf import settings

moderation_service = ModerationService(api_key=settings.GOOGLE_API_KEY)