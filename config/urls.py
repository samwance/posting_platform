from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('urls.user_urls')),
    path('posts/', include('urls.post_urls', namespace='posts')),
    path('posts/<int:post_id>/comments/', include('urls.comment_urls', namespace='comments')),
]
