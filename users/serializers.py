from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from users import models


class ProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=32)
    last_name = serializers.CharField(max_length=32)
    avatar = serializers.ImageField()
    last_login = serializers.DateTimeField()
    updated = serializers.DateTimeField()


class UserProfileSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 32)
    email = serializers.EmailField()
    profiles = ProfileSerializer()


class AdminProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length = 32)
    email = serializers.EmailField()
    password = serializers.CharField(max_length = 32)
    profiles = ProfileSerializer()
    