from django.urls import path
from .views import PostView, CommentView, LikeView, CommentReportView

urlpatterns = [
    path('', PostView.as_view(), name='posts'),
    path('<uuid:post_id>/', PostView.as_view(), name='post-detail'),
    path('<uuid:post_id>/comment/', CommentView.as_view(), name='post-comments'),
    path('<uuid:post_id>/comment/<uuid:comment_id>/', CommentView.as_view(), name='comment-delete'),
    path('<uuid:post_id>/comment/<uuid:comment_id>/report/', CommentReportView.as_view(), name='comment-delete'),
    path('<uuid:post_id>/like/', LikeView.as_view(), name='post-like'),
]
