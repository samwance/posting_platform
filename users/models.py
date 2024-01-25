from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    User - A model that reflects information about the user, including email,
    phone number, date of birth and account information (username, password, email, etc).
    """

    username = models.CharField(unique=True, max_length=255, verbose_name='login')
    email = models.EmailField(unique=True)
    phone_number = models.CharField(unique=True, max_length=17)
    birth_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
