from rest_framework import generics, status
from authorization import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from users import models
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(generics.CreateAPIView):
    serializer_class = serializers.RegisterSerializer


@api_view(['POST'])
def login_view(request):
    data = request.data
    try:
        user = models.Users.objects.get(username=data['username_email'])
    except models.Users.DoesNotExist:
        try:
            user = models.Users.objects.get(email=data['username_email'])
        except:
            return Response({"message": "Username or Email invalid!"}, status=status.HTTP_404_NOT_FOUND)
    if check_password(data['password'], user.password):
        refresh = RefreshToken.for_user(user)
        access_token =  str(refresh.access_token)
        if user.is_superuser:
            return Response({"message": "Admin logged in",
                             "access_token": access_token,
                             "refresh_token": str(refresh)}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "User logged in!",
                    "access_token": access_token,
                    "refresh_token": str(refresh) }, status=status.HTTP_200_OK)
    return Response({"message": "Password invalid!"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def change_password_view(request):
    serializer = serializers.ChangePasswordSerializer
    return Response({"message": str(request.user)})
