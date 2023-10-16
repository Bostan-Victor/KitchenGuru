from django.shortcuts import render
from rest_framework.decorators import api_view
from users import models
from authorization import serializers
from rest_framework import generics, status
from users import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
import recipes


class ProfileView(generics.RetrieveAPIView):
    serializer_class = serializers.ProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        data = self.request.data
        user = models.Users.objects.get(username = data['username'])
        return user


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

