from rest_framework import generics
from authorization import serializers


class RegisterView(generics.CreateAPIView):
    serializer_class = serializers.RegisterSerializer
