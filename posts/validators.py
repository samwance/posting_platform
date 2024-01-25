from rest_framework import serializers
from rest_framework.exceptions import ValidationError


def validate_title(value):
    forbidden_words = ['ерунда', 'глупость', 'чепуха']
    if any(word in value.lower() for word in forbidden_words):
        raise ValidationError('Title cannot contain forbidden words.')


