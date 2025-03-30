from rest_framework import serializers
from .models import Post, Likes, Comment
from user.serializers import UserProfileSerializer


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comment model with user profile information"""
    user = UserProfileSerializer(source='user_id', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'comment_id',
            'content',
            'user',
            'created_at'
        ]
        read_only_fields = [
            'comment_id',
            'created_at'
        ]


class LikeSerializer(serializers.ModelSerializer):
    """Serializer for like model with user profile information"""
    user = UserProfileSerializer(source='user_id', read_only=True)

    class Meta:
        model = Likes
        fields = [
            'like_id',
            'user',
            'created_at'
        ]
        read_only_fields = [
            'like_id',
            'created_at'
        ]


class PostSerializer(serializers.ModelSerializer):
    """Serializer for post model with nested relationships and counts"""
    user = UserProfileSerializer(source='user_id', read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    # image_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'post_id',
            'content',
            'image',
            'user',
            'likes_count',
            'comments_count',
            'comments',
            'created_at',
        ]
        read_only_fields = [
            'post_id',
            'created_at',
        ]

    def get_likes_count(self, obj) -> int:
        """Return count of likes for the post"""
        return obj.likes.count()

    def get_comments_count(self, obj) -> int:
        """Return count of comments for the post"""
        return obj.comments.count()

    def get_image_url(self, obj) -> str | None:
        """Return absolute URL for post image"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None
    