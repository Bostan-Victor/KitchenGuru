from users import models
from authorization import serializers
from rest_framework import generics
from superuser import serializers
from rest_framework.permissions import IsAuthenticated, IsAdminUser
# Create your views here.

class ProfileView(generics.ListAPIView):
    serializer_class = serializers.ProfileSerializer
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAdminUser]
    
    def get_object(self):
        data = self.request.data
        user = models.Users.objects.get(username = data['username'])
        return user
