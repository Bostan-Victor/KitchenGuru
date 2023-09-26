from rest_framework import serializers
from recipes import models


class CreateRecipeSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    ingredients = serializers.CharField(max_length=255)
    instructions = serializers.CharField(max_length=255)

    def create(self, validated_data):
        recipe = models.Recipes.objects.create(**validated_data)
        return recipe

class RecipeReviewSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    text = serializers.CharField(max_length=255)
    rating = serializers.IntegerField()
    
    
    def create(self, request):
        data = request
        user = request.user
        recipe = models.Recipes.objects.get(title=data["title"])
        review = models.Review.objects.create(recipes=recipe, user=user, rating=data["rating"], text=data["text"])
        return review
    
    