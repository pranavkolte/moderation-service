from rest_framework.views import APIView
from rest_framework import status
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from core.response import APIResponse
from .models import Post, Likes, Comment
from .serializers import PostSerializer, CommentSerializer, LikeSerializer


class PostView(APIView):
    """Handles post creation, retrieval, update, and deletion"""
    def get(self, request, post_id=None):
        """
        Retrieve single post (with caching) or all posts
        - Uses cache for single post retrieval
        - Orders all posts by creation date descending
        """
        if post_id:
            # Attempt cached post retrieval
            cache_key = f"post_{post_id}"
            try:
                if post_data := cache.get(cache_key):
                    return APIResponse.success(data=post_data)
            except Exception:
                pass

            post = get_object_or_404(Post, post_id=post_id)
            serializer = PostSerializer(post, context={'request': request})
            
            try:
                cache.set(cache_key, serializer.data)
            except Exception:
                pass
            
            return APIResponse.success(data=serializer.data)

        cache_key = f"all_posts{request.user.user_id}"
        try:
            if posts_data := cache.get(cache_key):
                return APIResponse.success(data=posts_data)
        except Exception:
            pass

        posts = Post.objects.all().order_by('-created_at')
        serializer = PostSerializer(
            posts, 
            many=True, 
            context={'request': request}
        )
        
        try:
            cache.set(cache_key, serializer.data)
        except Exception:
            pass

        return APIResponse.success(data=serializer.data)

    def post(self, request):
        """Create new post with user validation"""
        serializer = PostSerializer(
            data=request.data, 
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save(user_id=request.user)
            cache.delete(f"all_posts{request.user.user_id}")
            return APIResponse.success(
                message="Post created successfully",
                data=serializer.data,
                status_code=status.HTTP_201_CREATED
            )
        return APIResponse.validation_error(details=serializer.errors)

    def patch(self, request, post_id):
        """Update existing post with partial data"""
        post = get_object_or_404(Post, post_id=post_id, user_id=request.user)
        serializer = PostSerializer(
            post,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            cache.delete(f"post_{post_id}")
            cache.delete(f"all_posts{request.user.user_id}")
            return APIResponse.success(
                message="Post updated successfully",
                data=serializer.data
            )
        return APIResponse.validation_error(details=serializer.errors)

    def delete(self, request, post_id):
        """Delete post and clear related cache"""
        post = get_object_or_404(Post, post_id=post_id, user_id=request.user)
        post.delete()
        cache.delete(f"post_{post_id}")
        cache.delete(f"all_posts{request.user.user_id}")
        return APIResponse.success(message="Post deleted successfully")


class CommentView(APIView):
    """Manages post comments operations"""
    def get(self, request, post_id):
        """Retrieve all comments for a specific post"""
        comments = Comment.objects.filter(post_id=post_id)
        serializer = CommentSerializer(comments, many=True)
        return APIResponse.success(data=serializer.data)

    def post(self, request, post_id):
        """Add new comment to a post"""
        post = get_object_or_404(Post, post_id=post_id)
        serializer = CommentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(post_id=post, user_id=request.user)
            cache.delete(f"post_{post_id}")
            return APIResponse.success(
                message="Comment added successfully",
                data=serializer.data,
                status_code=status.HTTP_201_CREATED
            )
        return APIResponse.validation_error(details=serializer.errors)
    
    def patch(self, request, post_id, comment_id):
        """Update existing comment with partial data"""
        comment = get_object_or_404(
            Comment, 
            comment_id=comment_id,
            post_id=post_id,
            user_id=request.user
        )
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            cache.delete(f"post_{post_id}")
            return APIResponse.success(
                message="Comment updated successfully",
                data=serializer.data,
                status_code=status.HTTP_200_OK
            )
        return APIResponse.validation_error(details=serializer.errors)
    
    def delete(self, request, post_id, comment_id):
        """Delete comment and clear post cache"""
        comment = get_object_or_404(
            Comment, 
            comment_id=comment_id,
            post_id=post_id,
            user_id=request.user
        )
        comment.delete()
        cache.delete(f"post_{post_id}")
        return APIResponse.success(
            message="Comment deleted successfully",
            status_code=status.HTTP_200_OK
        )


class LikeView(APIView):
    """Handles post liking/unliking functionality"""
    def post(self, request, post_id):
        """Add like to post if not already liked"""
        post = get_object_or_404(Post, post_id=post_id)
        like, created = Likes.objects.get_or_create(
            post_id=post,
            user_id=request.user
        )
        
        if created:
            cache.delete(f"post_{post_id}")
            return APIResponse.success(message="Post liked successfully")
        
        return APIResponse.error(
            message="Post already liked",
            status_code=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, post_id):
        """Remove existing like from post"""
        like = get_object_or_404(Likes, post_id=post_id, user_id=request.user)
        like.delete()
        cache.delete(f"post_{post_id}")
        return APIResponse.success(message="Like removed successfully")
    