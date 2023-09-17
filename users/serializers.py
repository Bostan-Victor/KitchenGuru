from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from users import models


class ProfileSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 32)
    email = serializers.EmailField()
    password = serializers.CharField(max_length = 32)
    avatar = serializers.ImageField(default="static/avatars/no_picture.png")
    