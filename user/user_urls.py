from django.urls import path
from .views import UserProfileView

urlpatterns = [
    path('', UserProfileView.as_view(), name="user-view" ),
    path('<uuid:user_id>/', UserProfileView.as_view(), name="user-view" ),
]