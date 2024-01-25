from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="12345678",
            phone_number="12345678",
            birth_date="2003-01-01",
            is_staff=True,
            email="test@mail.ru"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_user(self):
        user_data = {
            "phone_number": "88888888",
            "username": "newuser",
            "birth_date": "2004-01-01",
            "email": "newuser@yandex.ru",
            "password": "12345678",
        }
        response = self.client.post(reverse("users:register"), user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_user_list(self):
        response = self.client.get(reverse("users:user_list"))
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_detail(self):
        user = User.objects.first()
        response = self.client.get(
            reverse("users:user_retrieve", kwargs={"pk": user.id})
        )
        serializer = UserSerializer(user)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        user = User.objects.first()
        updated_user = {
            "phone_number": "99999999",
            "username": "updateduser",
            "birth_date": "2005-01-01",
        }
        response = self.client.patch(
            reverse("users:user_update", kwargs={"pk": user.id}),
            updated_user,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        user = User.objects.first()
        response = self.client.delete(
            reverse("users:user_delete", kwargs={"pk": user.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class UserValidationTests(APITestCase):
    def test_register_invalid_email(self):
        user_data = {
            "phone_number": "88888888",
            "username": "newuser",
            "birth_date": "2004-01-01",
            "email": "newuser@nothing.ru",
            "password": "12345678",
        }
        response = self.client.post(reverse("users:register"), user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_invalid_password_digits(self):
        user_data = {
            "phone_number": "88888888",
            "username": "newuser",
            "birth_date": "2004-01-01",
            "email": "newuser@yandex.ru",
            "password": "qwertyuio",
        }
        response = self.client.post(reverse("users:register"), user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_invalid_password_length(self):
        user_data = {
            "phone_number": "88888888",
            "username": "newuser",
            "birth_date": "2004-01-01",
            "email": "newuser@yandex.ru",
            "password": "123",
        }
        response = self.client.post(reverse("users:register"), user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class IsOwnerPermissionsTests(APITestCase):
    def setUp(self):
        self.owner_user = User.objects.create_user(
            username="owneruser",
            password="12345678",
            phone_number="12345678",
            birth_date="2003-01-01",
            email="test@yandex.ru",
        )
        self.user = User.objects.create_user(
            username="testuser",
            password="123456789",
            phone_number="123456789",
            birth_date="2003-01-01",
            email="test2@yandex.ru",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_update_not_owner(self):
        user = User.objects.first()
        updated_user = {
            "phone_number": "99999999",
            "username": "updateduser",
            "birth_date": "2005-01-01",
        }
        response = self.client.patch(
            reverse("users:user_update", kwargs={"pk": user.id}),
            updated_user,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post_not_owner(self):
        user = User.objects.first()
        response = self.client.delete(
            reverse("users:user_delete", kwargs={"pk": user.id})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
