from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from users import models


class GetUserRecipes(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        images = obj.images.all()
        return GetRecipesImagesSerializer(images, many=True).data


class ProfileSerializer(serializers.Serializer):
    avatar = serializers.ImageField()


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 32)
    profile = ProfileSerializer(read_only=True)
    recipes = GetUserRecipes(many=True, read_only=True)


class UpdateAvatarSerializer(serializers.Serializer):
    avatar = serializers.ImageField()


class AddWatchListSerializer(serializers.Serializer):
    recipe_id = serializers.CharField(max_length=255)


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