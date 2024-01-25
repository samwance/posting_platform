from rest_framework import serializers

from users.models import User
from users.validators import validate_password, validate_email


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(validators=[validate_password])
    email = serializers.CharField(validators=[validate_email])

    class Meta:
        model = User
        fields = ("username", "email", "password", "birth_date", "phone_number")

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(validators=[validate_password])
    email = serializers.CharField(validators=[validate_email])

    class Meta:
        model = User
        fields = '__all__'
