from django.core.cache import cache

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer, OnboardUserSerializer, UserProfileSerializer
from .models import User
from core.response import APIResponse

class OnboardUserView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = OnboardUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserProfileView(APIView):
    def get(self, request, user_id=None):
        if user_id:
            cache_key = f"user_profile_{user_id}"
            try:
                user_pofile_data = cache.get(cache_key)
                if user_pofile_data:
                    cache.set(cache_key, user_pofile_data)
                    return APIResponse.success(
                        message="User profile retrieved successfully",
                        data=user_pofile_data,
                        status_code=status.HTTP_200_OK,
                    )
            except Exception as e:
                pass 
            user = User.objects.get(user_id=user_id)
        else:
            user = request.user
            if not user:
               return APIResponse.not_found(message="User not found")
        
        cache_key = f"user_profile_{user.user_id}"
        try:
            user_pofile_data = cache.get(cache_key)
            if user_pofile_data:
                cache.set(cache_key, user_pofile_data)
                return APIResponse.success(
                    message="User profile retrieved successfully",
                    data=user_pofile_data,
                    status_code=status.HTTP_200_OK,
                )
        except Exception as e:
            pass    
        
        user_profile_data = UserProfileSerializer(user, context={'request': request}).data
        try:
            cache.set(cache_key, user_profile_data)
        except Exception as e:
            pass
        
        return APIResponse.success(
            message="User profile retrieved successfully",
            data=user_profile_data,
            status_code=status.HTTP_200_OK,
        )

    def patch(self, request):
        
        user = request.user

        serializer = UserProfileSerializer(user, data=request.data, partial=True, context={'request': request})
        
        if serializer.is_valid():
            try:
                updated_user = serializer.save()
                
                # Update cache
                cache_key = f"user_profile_{user.user_id}"
                cache.delete(cache_key)  # Delete old cache
                user_profile_data = UserProfileSerializer(updated_user).data
                
                return APIResponse.success(
                    message="User profile updated successfully",
                    data=user_profile_data,
                    status_code=status.HTTP_200_OK
                )
            except Exception as e:
                return APIResponse.error(
                    message="Failed to update user profile",
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    details=str(e)
                )
        
        return APIResponse.validation_error(
            message="Invalid data provided",
            details=serializer.errors
        )