from django.urls import path

from posts.apps import PostsConfig
from posts.views import PostCreate, PostList, PostDetail, PostUpdate, PostDelete

app_name = PostsConfig.name

urlpatterns = [
    path("create/", PostCreate.as_view(), name="post_create"),
    path("", PostList.as_view(), name="post_list"),
    path("<int:pk>/", PostDetail.as_view(), name="post_retrieve"),
    path("<int:pk>/update/", PostUpdate.as_view(), name="post_update"),
    path("<int:pk>/delete/", PostDelete.as_view(), name="post_delete"),
]
