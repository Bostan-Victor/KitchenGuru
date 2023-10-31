from django.shortcuts import render
from rest_framework.decorators import api_view
from users import models
from authorization import serializers
from rest_framework import generics, status
from users import serializers
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.utils import timezone
from users import models
from users import serializers
import recipes
import logging
import logging.config
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, '..', 'KitchenGuru', 'user_activity.conf')
logging.config.fileConfig(config_path, disable_existing_loggers=False)
USER_LOGGER = logging.getLogger('user')
config_path = os.path.join(current_dir, '..', 'KitchenGuru', 'system_activity.conf')
logging.config.fileConfig(config_path, disable_existing_loggers=False)
SYSTEM_LOGGER = logging.getLogger('activity')


class ProfileView(generics.RetrieveAPIView):
    serializer_class = serializers.UserProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_object(self):
        data = self.request.query_params.get('username', '')
        if data != '':
            try:
                user = models.Users.objects.get(username=data)
            except models.Users.DoesNotExist:
                USER_LOGGER.error(f"User with username={data} was not found.")
                SYSTEM_LOGGER.warning(f'User with username={data} was not found!')
                raise models.Users.DoesNotExist(f'User with username={data} was not found!')
        else:
            if not self.request.user.is_anonymous:
                user = self.request.user
            else:
                raise PermissionError('Access token was not provided!')
        try:
            profile = models.Profiles.objects.get(user=user)
        except models.Profiles.DoesNotExist:
            USER_LOGGER.error(f"User with user_id={user.id} tried to access profile but their profile wasn't found.")
            SYSTEM_LOGGER.warning(f'Profile for user_id={user.id} was not found!')
            return Response({'message': f'Profile for user_id={user.id} was not found!'}, status=status.HTTP_404_NOT_FOUND)
        user_created_recipes = recipes.models.Recipes.objects.filter(created_by_id=user.id)
        user_data = {
            'username': user.username,
            'email': user.email,
            'profile': {
                'avatar': profile.avatar
            },
            'recipes': user_created_recipes
        }
        USER_LOGGER.info(f"User with user_id={user.id} accessed their profile.")
        return user_data


class AddWatchListView(generics.CreateAPIView):
    serializer_class = serializers.AddWatchListSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        user = request.user
        recipe_id = request.query_params.get('recipe_id')

        if recipe_id is None:
            USER_LOGGER.error(f"User with user_id={user.id} tried to add recipe to watch list without providing recipe_id.")
            return Response({'message': 'The recipe_id query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            recipe = recipes.models.Recipes.objects.get(id=recipe_id)
        except recipes.models.Recipes.DoesNotExist:
            USER_LOGGER.warning(f"User with user_id={user.id} tried to add non-existent recipe with id={recipe_id} to watch list.")
            return Response({'message': 'This recipe does not exist!'}, status=status.HTTP_404_NOT_FOUND)

        recipe, created = models.WatchList.objects.get_or_create(user=user, recipe=recipe)
        if not created:
            recipe.viewed_at = timezone.now()
            recipe.save()
            USER_LOGGER.info(f"User with user_id={user.id} viewed the recipe with id={recipe_id} again. View time updated.")
            SYSTEM_LOGGER.info(f'The viewed at time of the recipe with id {recipe_id} was updated to the watchlist of user with id {user.id}')
            return Response({"message": "Recipe viewed at time updated!"}, status=status.HTTP_200_OK)
        USER_LOGGER.info(f"User with user_id={user.id} added the recipe with id={recipe_id} to their watch list.")
        SYSTEM_LOGGER.info(f'Recipe with id {recipe_id} was added to the watchlist of user with id {user.id}')
        return Response({'message': 'Recipe added to watch list!'}, status=status.HTTP_201_CREATED)


class RecentRecipesView(generics.ListAPIView):
    serializer_class = serializers.GetRecipesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        watch_entries = models.WatchList.objects.filter(user=user).order_by('-viewed_at')
        recent_recipes = [entry.recipe for entry in watch_entries]
        return recent_recipes
    

class UpdateProfileView(generics.UpdateAPIView):
    serializer_class = serializers.UpdateProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profiles
