import requests
from django.conf import settings

class ModerationService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = settings.MODERATION_API_URL
        if not self.base_url:
            raise ValueError("Moderation API URL is not set in settings.")
        if not self.api_key:
            raise ValueError("API key is required for moderation service.")

    def moderate_text(self, text):
        url = f"{self.base_url}?key={self.api_key}"
        payload = {
            "document": {
                "type": "PLAIN_TEXT",
                "content": text
            }
        }
        headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }

        response = requests.post(url, json=payload, headers=headers)
        return response.json()
