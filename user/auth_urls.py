from django.urls import path
from .views import OnboardUserView, CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
    path("signup/", OnboardUserView.as_view(), name="onboard_user"),
    path("signin/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
]