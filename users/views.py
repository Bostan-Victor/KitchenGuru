from django.shortcuts import render
from rest_framework.decorators import api_view
from authorization import serializers
from rest_framework import generics
from users import serializers
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Create your views here.

class ProfileView(generics.RetrieveAPIView):
    serializer_class = serializers.ProfileSerializer
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAdminUser]
    
    def get_object(self):
        return self.request.user

