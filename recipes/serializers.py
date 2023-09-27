from rest_framework import serializers
from recipes import models


class CreateRecipesImageSerializer(serializers.Serializer):
    image = serializers.ImageField()

    def create(self, validated_data, *args, **kwargs):
        img = models.RecipesImages.objects.create(**validated_data)
        return img


class CreateRecipeSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    ingredients = serializers.CharField(max_length=255)
    instructions = serializers.CharField(max_length=255)
    image = serializers.ImageField()
    images = CreateRecipesImageSerializer(many=True, write_only=True, required=False)

    def create(self, validated_data, *args, **kwargs):
        image_data = validated_data.pop('images', [])
        recipe = models.Recipes.objects.create(**validated_data)
        
        for image in image_data:
            image['recipe'] = recipe
            CreateRecipesImageSerializer().create(validated_data=image)

        return recipe


class RecipeReviewSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=255)
    rating = serializers.IntegerField()