from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from users import models
from django.conf import settings
    

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


class ProfileSerializer(serializers.Serializer):
    avatar = serializers.ImageField()


class UserProfileSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 32)
    email = serializers.EmailField()
    profile = ProfileSerializer(read_only=True)
    recipes = GetRecipesSerializer(many=True, read_only=True)


class AddWatchListSerializer(serializers.Serializer):
    recipe_id = serializers.IntegerField()
    
    
class GetRecipesImagesSerializer(serializers.Serializer):
    image = serializers.ImageField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Users
        fields = ['username', 'email']


class UpdateProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    class Meta:
        model = models.Profiles
        fields = ['avatar', 'user']
        depth = 1

    def update(self, instance, validated_data):
        instance.user.username = self.initial_data.get('username', instance.user.username)
        instance.user.email = self.initial_data.get('email', instance.user.email)
        instance.avatar = self.initial_data.get('avatar', instance.avatar)
        instance.user.save()
        instance.save()

        return self.to_representation(instance)
    
    def to_representation(self, instance):
        data = {}
        data['username'] = self.context['request'].user.username
        data['email'] = self.context['request'].user.email
        data['avatar'] = self.context['request'].user.profiles.avatar.url
        return data
