from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

class OnboardUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password', 'date_of_birth']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["email"] = self.user.email
        return data
    
class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["message"] = "Token refreshed successfully"
        return data
    
from django.conf import settings

class UserProfileSerializer(serializers.ModelSerializer):
    profile_picture_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'name', 'bio', 'profile_picture', 'profile_picture_url', 'date_of_birth', 'post_count']
        read_only_fields = ['user_id', 'created_at', 'updated_at', 'post_count']
        extra_kwargs = {
            'profile_picture': {'write_only': True, 'required': False},
        }

    def get_profile_picture_url(self, obj):
        if obj.profile_picture:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.profile_picture.url)
            return f"{settings.SITE_URL}{obj.profile_picture.url}"
        return None