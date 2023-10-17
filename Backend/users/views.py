from django.shortcuts import render
from rest_framework.decorators import api_view
from users import models
from authorization import serializers
from rest_framework import generics, status
from users import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from users import models
from users import serializers
from datetime import datetime
import recipes


class ProfileView(generics.RetrieveAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        user_id = self.request.user.id
        try:
            user = models.Users.objects.get(id=user_id)
        except models.Users.DoesNotExist:
            return Response({'message': f'User with user_id={user_id} was not found!'}, status=status.HTTP_404_NOT_FOUND)
        try:
            profile = models.Profiles.objects.get(user=user)
        except models.Profiles.DoesNotExist:
            return Response({'message': f'Profile for user_id={user_id} was not found!'}, status=status.HTTP_404_NOT_FOUND)
        user_created_recipes = recipes.models.Recipes.objects.filter(created_by_id=user_id)
        user_data = {
            'username': user.username,
            'profile': {
                'avatar': profile.avatar
            },
            'recipes': user_created_recipes
        }
        return user_data
    

class UpdateAvatarView(generics.UpdateAPIView):
    serializer_class = serializers.UpdateAvatarSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request):
        user_id = request.user.id
        avatar = request.data['avatar']
        if not avatar:
            return Response({'message': 'A new avatar was not provided!'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user_profile = models.Profiles.objects.get(user_id=user_id)
        except models.Profiles.DoesNotExist:
            return Response({'message': f'Profile for user_id={user_id} was not found!'}, status=status.HTTP_404_NOT_FOUND)

        user_profile.avatar = avatar
        user_profile.updated = datetime.now()
        user_profile.save()
        return Response({'new_avatar': user_profile.avatar.url}, status=status.HTTP_200_OK)


class AddWatchListView(generics.CreateAPIView):
    serializer_class = serializers.AddWatchListSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        user = request.user
        recipe_id = request.query_params.get('recipe_id')

        if recipe_id is None:
            return Response({'message': 'The recipe_id query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            recipe = recipes.models.Recipes.objects.get(id=recipe_id)
        except recipes.models.Recipes.DoesNotExist:
            return Response({'message': 'This recipe does not exist!'}, status=status.HTTP_404_NOT_FOUND)

        recipe, created = models.WatchList.objects.get_or_create(user=user, recipe=recipe)
        if not created:
            recipe.viewed_at = timezone.now()
            recipe.save()
        return Response({'message': 'Recipe added to watch list!'}, status=status.HTTP_201_CREATED)



class RecentRecipesView(generics.ListAPIView):
    serializer_class = serializers.GetRecipesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        watch_entries = models.WatchList.objects.filter(user=user).order_by('-viewed_at')
        recent_recipes = [entry.recipe for entry in watch_entries]
        return recent_recipes

