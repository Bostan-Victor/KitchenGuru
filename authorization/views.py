from rest_framework import generics
from authorization import serializers
from users import models


class RegisterView(generics.CreateAPIView):
    serializer_class = serializers.RegisterSerializer


class LoginView(generics.ListCreateAPIView):
    queryset = models.Users.objects.all()
    serializer_class = serializers.LoginSerializer
