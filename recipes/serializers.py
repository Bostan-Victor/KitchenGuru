from rest_framework import serializers
from recipes import models


class CreateRecipeSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    ingredients = serializers.CharField(max_length=255)
    instructions = serializers.CharField(max_length=255)

    def create(self, validated_data):
        recipe = models.Recipes.objects.create(**validated_data)
        return recipe
