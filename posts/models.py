from django.db import models

from users.models import User


class Post(models.Model):
    """
    Post - A model that represents a post created by a user.
    It contains information about the title, text, image (if there is one), and the user who created the post.
    """

    title = models.CharField(max_length=255)
    text = models.TextField()
    image = models.ImageField(upload_to="posts/", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'


class Comment(models.Model):
    """
    Comment - A model that represents a comment added by a user to a post.
    It contains information about the user who added the comment, the post it refers to,
    and the text of the comment.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentator")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
