from rest_framework import serializers
from recipes import models
from datetime import datetime
import logging
import logging.config
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, '..', 'KitchenGuru', 'system_activity.conf')
logging.config.fileConfig(config_path, disable_existing_loggers=False)
SYSTEM_LOGGER = logging.getLogger('activity')


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
        image_data = self.context['request'].FILES.pop('image', None)
        recipe = models.Recipes.objects.create(**validated_data)
        image_instances = []

        for image in image_data:
            image_instances.append(models.RecipesImages(recipe=recipe, image=image))

        models.RecipesImages.objects.bulk_create(image_instances, len(image_instances))

        return recipe
    

class AIRecipeSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=255)
    image_url = serializers.CharField(max_length=255)


class UserSerializer(serializers.Serializer):
    avatar = serializers.ImageField(source='profiles.avatar')
    username = serializers.CharField(max_length=32)


class ReviewDetailSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=255)
    rating = serializers.IntegerField()
    user = UserSerializer()

    def to_representation(self, instance):
        data = {}
        data['text'] = instance.text
        data['rating'] = instance.rating
        data['username'] = instance.user.username
        data['avatar'] = instance.user.profiles.avatar.url
        return data


class AdminReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = '__all__'
        depth = 1

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            SYSTEM_LOGGER.warning(f"Rating validation failed. Given rating: {value}.")
            raise serializers.ValidationError("Rating should be between 1 and 5.")
        return value

    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating', instance.rating)
        instance.text = validated_data.get('text', instance.text)
        instance.review_date = validated_data.get('review_added', datetime.now())
        instance.save()
        SYSTEM_LOGGER.info(f"Review with ID: {instance.id} was updated by a superuser.")
        return instance

    def delete(self, instance):
        SYSTEM_LOGGER.info(f"Review with ID: {instance.id} was deleted by a superuser.")
        instance.delete()

    def to_representation(self, instance):
        data = {}
        data['review_id'] = instance.id
        data['text'] = instance.text
        data['rating'] = instance.rating
        data['recipe_id'] = instance.recipes.id
        data['user_id'] = instance.user.id
        data['username'] = instance.user.username
        data['avatar'] = instance.user.profiles.avatar.url
        return data


class UserReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = ['rating', 'text']

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            SYSTEM_LOGGER.warning(f"Rating validation failed. Given rating: {value}.")
            raise serializers.ValidationError("Rating should be between 1 and 5.")
        return value

    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating', instance.rating)
        instance.text = validated_data.get('text', instance.text)
        instance.review_date = datetime.now()
        instance.save()
        SYSTEM_LOGGER.info(f"Review with ID: {instance.id} was updated by user with ID {instance.user.id}.")
        return instance

    def delete(self, instance):
        SYSTEM_LOGGER.info(f"Review with ID: {instance.id} was deleted by user with ID {instance.user.id}.")
        instance.delete()

    def to_representation(self, instance):
        data = {}
        data['text'] = instance.text
        data['rating'] = instance.rating
        data['username'] = instance.user.username
        data['avatar'] = instance.user.profiles.avatar.url
        return data


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
    created_by = serializers.CharField(max_length=255)
    
    def get_images(self, obj):
        images = obj.images.all()
        return GetRecipesImagesSerializer(images, many=True).data
    

class GetIngredientsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)


class SearchRecipesSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='recipe.id')
    title = serializers.CharField(source='recipe.title', max_length=255)
    ingredients = serializers.CharField(source='recipe.ingredients', max_length=255)
    instructions = serializers.CharField(source='recipe.instructions', max_length=255)
    category = serializers.CharField(source='recipe.category', max_length=10)
    duration = serializers.IntegerField(source='recipe.duration')
    ingredient_tags = serializers.CharField(source='recipe.ingredient_tags', max_length=255)
    images = serializers.SerializerMethodField()
    matching_ingredients = serializers.CharField(max_length=255)
    missing_ingredients = serializers.CharField(max_length=255)

    def get_images(self, obj):
        images = obj['recipe'].images.all()
        return GetRecipesImagesSerializer(images, many=True).data
    
    
class RecipeIdSerialier(serializers.Serializer):
    recipe_id = serializers.CharField(max_length=255)


class FilterRecipesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    ingredients = serializers.CharField(max_length=255)
    instructions = serializers.CharField(max_length=255)
    category = serializers.CharField(max_length=10)
    duration = serializers.IntegerField()
    ingredient_tags = serializers.CharField(max_length=255)
    images = serializers.SerializerMethodField()
    favorites_count = serializers.IntegerField()
    review_count = serializers.IntegerField()
    average_rating = serializers.FloatField()
    
    def get_images(self, obj):
        images = obj.images.all()
        return GetRecipesImagesSerializer(images, many=True).data
    
