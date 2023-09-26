from rest_framework import generics
from recipes import serializers
from rest_framework.permissions import IsAuthenticated


class CreateRecipeView(generics.CreateAPIView):
    serializer_class = serializers.CreateRecipeSerializer
    permission_classes = [IsAuthenticated]

