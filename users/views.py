from django.shortcuts import render
from rest_framework.decorators import api_view
from users import models

from authorization import serializers
from rest_framework import generics
from users import serializers
from rest_framework import permissions

# Create your views here.

class ProfileView(generics.ListAPIView):
    queryset = models.Profiles.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

