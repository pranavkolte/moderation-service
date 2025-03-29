import uuid

from django.db import models
from django.conf import settings


class Post(models.Model):
    post_id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        db_index=True
    )
    content = models.TextField()
    image = models.ImageField(
        upload_to='post_images/',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'post'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user_id', 'created_at']),
        ]

    def __str__(self) -> str:
        return f"Post {self.post_id} by {self.user_id}"


class Likes(models.Model):
    like_id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )
    post_id = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='likes',
        db_index=True
    )
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes',
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'likes'
        ordering = ['-created_at']
        unique_together = ('post_id', 'user_id')
        indexes = [
            models.Index(fields=['post_id', 'user_id']),
        ]

    def __str__(self) -> str:
        return f"Like {self.like_id} on Post {self.post_id} by {self.user_id}"


class Comment(models.Model):
    comment_id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )
    post_id = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='comments',
        db_index=True
    )
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        db_index=True
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comment'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['post_id', 'created_at']),
        ]

    def __str__(self) -> str:
        return f"Comment {self.comment_id} on Post {self.post_id} by {self.user_id}"
    