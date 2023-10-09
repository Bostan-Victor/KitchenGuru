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
    category = serializers.CharField(max_length=10)
    duration = serializers.IntegerField()
    ingredient_tags = serializers.CharField(max_length=255)
    image = CreateRecipesImageSerializer(many=True, write_only=True, required=False)

    def create(self, validated_data, *args, **kwargs):
        image_data = validated_data.pop('image', [])
        recipe = models.Recipes.objects.create(**validated_data)
        image_instances = []

        for image in image_data:
            image_instances.append(models.RecipesImages(recipe=recipe, **image))

        models.RecipesImages.objects.bulk_create(image_instances, len(image_instances))

        return recipe


class RecipeReviewSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=255)
    rating = serializers.IntegerField()


class GetRecipesImagesSerializer(serializers.Serializer):
    image = serializers.ImageField()


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
    

class GetIngredientsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)


class AddFavoritesSerialier(serializers.Serializer):
    recipe_id = serializers.CharField(max_length=255)
