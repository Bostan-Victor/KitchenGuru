from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from users import models


class ProfileSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 32)
    email = serializers.EmailField()
    password = serializers.CharField(max_length = 32)
    avatar = serializers.ImageField(default="static/avatars/no_picture.png")


class AddAvatarSerializer(serializers.Serializer):
    avatar = serializers.ImageField(default="static/avatars/no_picture.png")


class AddWatchListSerializer(serializers.Serializer):
    recipe_id = serializers.IntegerField()


class GetRecipesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    ingredients = serializers.CharField(max_length=255)
    instructions = serializers.CharField(max_length=255)
    category = serializers.CharField(max_length=10)
    duration = serializers.IntegerField()
    ingredient_tags = serializers.CharField(max_length=255)
    images = serializers.SerializerMethodField()
    
    def get_images(self, obj):
        images = obj.images.all()
        return GetRecipesImagesSerializer(images, many=True).data
    
    
class GetRecipesImagesSerializer(serializers.Serializer):
    image = serializers.ImageField()