from datetime import date, datetime

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, viewsets, serializers
from rest_framework.response import Response
from rest_framework.views import status
from .models import Post, Comment
from .permissions import IsOwner
from .serializers import PostSerializer, CommentSerializer, CommentCreateSerializer


class PostCreate(generics.CreateAPIView):
    """
    Create a new post.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Check if the user is old enough to create a post.
        """
        today = date.today()
        birth_date_str = str(self.request.user.birth_date)
        birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
        age = (
            today.year
            - birth_date.year
            - ((today.month, today.day) < (birth_date.month, birth_date.day))
        )
        if age < 18:
            raise ValidationError(
                "User must be at least 18 years old to create a post."
            )
        serializer.save(user=self.request.user)


class PostList(generics.ListAPIView):
    """
    List all posts.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveAPIView):
    """
    Retrieve a post.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostUpdate(generics.UpdateAPIView):
    """
    Update a post.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAdminUser | IsOwner]

    def perform_update(self, serializer):
        """
        Check if the user has permission to edit the post.
        """
        post = self.get_object()
        if post.user != self.request.user and not self.request.user.is_staff:
            return Response(
                {"message": "You do not have permission to edit this post."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer.save()


class PostDelete(generics.DestroyAPIView):
    """
    Delete a post.
    """

    queryset = Post.objects.all()
    permission_classes = [permissions.IsAdminUser | IsOwner]

    def delete(self, request, *args, **kwargs):
        """
        Check if the user has permission to delete the post.
        """
        post = self.get_object()
        if not request.user.is_staff and post.user != request.user:
            return Response(
                {"message": "You do not have permission to delete this post."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return self.destroy(request, *args, **kwargs)


class CommentCreate(generics.CreateAPIView):
    """
    Create a new comment.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer, *args, **kwargs):
        """
        Check if the post exists.
        """
        post_id = self.kwargs.get("post_id")
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise serializers.ValidationError(
                f"There's no any post with given id {post_id}"
            )
        serializer.save(
            user=self.request.user, post=post, text=self.request.data.get("text")
        )


class CommentList(generics.ListAPIView):
    """
    List all comments.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentDetail(generics.RetrieveAPIView):
    """
    Retrieve a comment.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentUpdate(generics.UpdateAPIView):
    """
    Update a comment.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAdminUser | IsOwner]

    def perform_update(self, serializer):
        """
        Check if the user has permission to edit the comment.
        """
        post = self.get_object()
        if post.user != self.request.user and not self.request.user.is_staff:
            return Response(
                {"message": "You do not have permission to edit this comment."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer.save()


class CommentDelete(generics.DestroyAPIView):
    """
    Delete a comment.
    """

    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAdminUser | IsOwner]

    def delete(self, request, *args, **kwargs):
        """
        Check if the user has permission to delete the comment.
        """
        post = self.get_object()
        if not request.user.is_staff and post.user != request.user:
            return Response(
                {"message": "You do not have permission to delete this comment."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return self.destroy(request, *args, **kwargs)
