from rest_framework import serializers


def validate_email(email):
    if not email.endswith("@mail.ru") and not email.endswith("@yandex.ru"):
        raise serializers.ValidationError(
            'Only "mail.ru" and "yandex.ru" domains allowed'
        )


def validate_password(password):
    if len(password) < 8 or not any(char.isdigit() for char in password):
        raise serializers.ValidationError(
            "The password must be at least 8 characters and must include numbers"
        )
