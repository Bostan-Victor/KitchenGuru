from authorization import serializers
from rest_framework import generics
from superuser import serializers
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from users import models

# Create your views here.

class AdminView(generics.ListAPIView):
    queryset = models.Users.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAdminUser]
    
    def get_object(self):
        return self.request.user