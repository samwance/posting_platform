from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class PostTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            phone_number="12345678",
            birth_date="2003-01-01",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.post_data = {
            "title": "Test Post",
            "text": "This is a test post.",
            "user": self.user.id,
        }
        self.response = self.client.post(
            reverse("posts:post_create"), self.post_data, format="json"
        )

    def test_create_post(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_get_post_list(self):
        response = self.client.get(reverse("posts:post_list"))
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_post_detail(self):
        post = Post.objects.first()
        response = self.client.get(
            reverse("posts:post_retrieve", kwargs={"pk": post.id})
        )
        serializer = PostSerializer(post)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_post(self):
        post = Post.objects.first()
        updated_post = {"title": "Updated Post", "text": "This is an updated post."}
        response = self.client.patch(
            reverse("posts:post_update", kwargs={"pk": post.id}),
            updated_post,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_post(self):
        post = Post.objects.first()
        response = self.client.delete(
            reverse("posts:post_delete", kwargs={"pk": post.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CommentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            phone_number="12345678",
            birth_date="2003-01-01",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(
            title="Test Post", text="This is a test post.", user=self.user
        )
        self.comment_data = {
            "text": "This is a test comment.",
            "user": self.user.id,
            "post": self.post.id,
        }
        self.response = self.client.post(
            reverse("comments:comment_create", kwargs={"post_id": self.post.id}),
            self.comment_data,
            format="json",
        )

    def test_create_comment(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_get_comment_list(self):
        response = self.client.get(
            reverse("comments:comment_list", kwargs={"post_id": self.post.id})
        )
        comments = Comment.objects.filter(post=self.post)
        serializer = CommentSerializer(comments, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_comment_detail(self):
        comment = Comment.objects.first()
        response = self.client.get(
            reverse(
                "comments:comment_retrieve",
                kwargs={"post_id": self.post.id, "pk": comment.id},
            )
        )
        serializer = CommentSerializer(comment)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_comment(self):
        comment = Comment.objects.first()
        updated_comment = {"text": "This is an updated comment."}
        response = self.client.patch(
            reverse(
                "comments:comment_update",
                kwargs={"post_id": self.post.id, "pk": comment.id},
            ),
            updated_comment,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_comment(self):
        comment = Comment.objects.first()
        response = self.client.delete(
            reverse(
                "comments:comment_delete",
                kwargs={"post_id": self.post.id, "pk": comment.id},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PostValidationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            phone_number="12345678",
            birth_date="2003-01-01",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_post_valid_data(self):
        post_data = {
            "title": "Test Post",
            "text": "This is a test post.",
            "user": self.user.id,
        }
        response = self.client.post(
            reverse("posts:post_create"), post_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_post_underage_user(self):
        underage_user = User.objects.create_user(
            username="underage_user",
            password="testpass",
            phone_number="1234567",
            birth_date="2015-02-23",
            email="test@yandex.ru"
        )
        client = APIClient()
        client.force_authenticate(user=underage_user)
        post_data = {
            "title": "Test Post",
            "text": "This is a test post.",
            "user": underage_user.id,
        }
        response = client.post(
            reverse("posts:post_create"), post_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_post_no_title(self):
        post_data = {"text": "This is a test post.", "user": self.user.id}
        response = self.client.post(
            reverse("posts:post_create"), post_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_create_post_forbidden_word(self):
        post_data = {
            "title": "ерунда",
            "text": "This is a test post.",
            "user": self.user.id,
        }
        response = self.client.post(
            reverse("posts:post_create"), post_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)


class CommentValidationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            phone_number="12345678",
            birth_date="2003-01-01",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(
            title="Test Post", text="This is a test post.", user=self.user
        )
        self.comment_data = {
            "text": "This is a test comment.",
            "user": self.user.id,
            "post": self.post.id,
        }
        self.response = self.client.post(
            reverse("comments:comment_create", kwargs={"post_id": self.post.id}),
            self.comment_data,
            format="json",
        )

    def test_create_comment_valid_data(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_create_comment_no_text(self):
        comment_data = {"user": self.user.id, "post": self.post.id}
        response = self.client.post(
            reverse("comments:comment_create", kwargs={"post_id": self.post.id}),
            comment_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("text", response.data)

    def test_create_comment_no_post(self):
        comment_data = {"text": "This is a test comment.", "user": self.user.id}
        response = self.client.post(
            reverse("comments:comment_create", kwargs={"post_id": 100}),
            comment_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PermissionsTests(APITestCase):
    def setUp(self):
        self.owner_user = User.objects.create_user(
            username="owneruser",
            password="testpass1",
            phone_number="12345678",
            birth_date="2003-01-01",
            email="test@yandex.ru",
        )
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            phone_number="123456789",
            birth_date="2003-01-01",
            email="test2@yandex.ru",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(
            title="Test Post", text="This is a test post.", user=self.owner_user
        )
        self.comment = Comment.objects.create(
            text="This is a test comment.", user=self.owner_user, post=self.post
        )

    def test_update_post_not_owner(self):
        post = Post.objects.first()
        updated_post = {"title": "Updated Post", "text": "This is an updated post."}
        response = self.client.patch(
            reverse("posts:post_update", kwargs={"pk": post.id}),
            updated_post,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_comment_not_owner(self):
        comment = Comment.objects.first()
        updated_comment = {"text": "This is an updated comment."}
        response = self.client.patch(
            reverse(
                "comments:comment_update",
                kwargs={"post_id": self.post.id, "pk": comment.id},
            ),
            updated_comment,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_comment_not_owner(self):
        comment = Comment.objects.first()
        response = self.client.delete(
            reverse(
                "comments:comment_delete",
                kwargs={"post_id": self.post.id, "pk": comment.id},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post_not_owner(self):
        post = Post.objects.first()
        response = self.client.delete(
            reverse("posts:post_delete", kwargs={"pk": post.id})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
