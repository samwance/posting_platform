from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from posts.models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
    list_filter = ("created_at",)

    def view_the_author(self, obj):
        if obj.user:
            url = reverse("admin:user_user_change", args=[obj.user.pk])
            return format_html('<a href="{}">{}</a>', url, obj.user.username)
        return "-"

    view_the_author.short_description = "Author"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
