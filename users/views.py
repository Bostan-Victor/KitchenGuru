from authorization import serializers
from rest_framework import generics
from users import serializers
from rest_framework import permissions
from users import models
from rest_framework.response import Response
from rest_framework import status


class ProfileView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]


    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return serializers.AdminProfileSerializer
        return serializers.UserProfileSerializer
    

    def list(self, request):
        user = request.user

        if user.is_superuser:
            queryset = models.Users.objects.all().select_related('profiles')
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            if request.method in permissions.SAFE_METHODS:
                queryset = models.Users.objects.get(id=user.id)
                serializer = self.get_serializer(queryset, many=False)
                return Response(serializer.data, status=status.HTTP_200_OK)
