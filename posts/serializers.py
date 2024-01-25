from rest_framework import serializers

from posts.models import Post, Comment
from posts.validators import validate_title


class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators=[validate_title])

    class Meta:
        model = Post
        fields = "__all__"


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("text",)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
