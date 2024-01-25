from django.urls import path

from posts.apps import PostsConfig
from posts.views import CommentCreate, CommentList, CommentUpdate, CommentDelete, CommentDetail

app_name = PostsConfig.name

urlpatterns = [
    path("create/", CommentCreate.as_view(), name="comment_create"),
    path("", CommentList.as_view(), name="comment_list"),
    path("<int:pk>/", CommentDetail.as_view(), name="comment_retrieve"),
    path("<int:pk>/update/", CommentUpdate.as_view(), name="comment_update"),
    path("<int:pk>/delete/", CommentDelete.as_view(), name="comment_delete"),
]
