from rest_framework import generics, status
from authorization import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from users import models
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from datetime import datetime, timedelta
import random


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
    try:
        profile = models.Profiles.objects.get(user_id=user.id)
        profile.last_login = datetime.now()
        profile.save()
    except:
        return Response({"message": "Profile does not exist!"}, status=status.HTTP_404_NOT_FOUND)
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


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = serializers.ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        data = request.data
        user = request.user

        if check_password(data['password'], user.password):
            if len(data['new_password']) < 8:
                return Response({"message": "Password shorter than 8 characters"}, status=status.HTTP_400_BAD_REQUEST)
            if data['new_password'] != data['confirm_new_password']:
                return Response({"message": "New password fields do not match!"}, status=status.HTTP_400_BAD_REQUEST)
            new_password = data['new_password']
            user.set_password(new_password)
            user.save()
            profile = models.Profiles.objects.get(user_id=user.id)
            profile.updated = datetime.now()
            profile.save()
            return Response({"message": "Password updated succesfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Old password is incorrect!"}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
def password_recovery_request_view(request):
    data = request.data
    try:
        user = models.Users.objects.get(email=data['email'])
    except:
        return Response({'message': 'There is no account created with this email!'}, status=status.HTTP_404_NOT_FOUND)
    pass_reset_code = models.PasswordResetCode.objects.get(user_id=user.id)
    code = str(random.randint(100000, 999999))
    pass_reset_code.code = code
    pass_reset_code.created_at = datetime.now()
    pass_reset_code.save()
    send_mail(
        'KitchenGuru - Password reset code',
        f'Your 6-digit code:\n{code}',
        'KitchenGuru@mail.com',
        [data['email']],
        fail_silently=False
    )
    return Response({'message': 'Email sent succesfully!'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def password_recovery_confirm_view(request):
    data = request.data
    delta = timedelta(minutes=5)

    if len(data['code']) > 6:
        return Response({'message': 'The code is not the right length!'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        user = models.Users.objects.get(email=data['email'])
        pass_reset_object = models.PasswordResetCode.objects.get(user_id=user.id)
        created_at = pass_reset_object.created_at.replace(tzinfo=None)
        now = datetime.now()

        if created_at - now > delta:
            return Response({'message': 'The code has expired!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if data['code'] != pass_reset_object.code:
                return Response({'messasge': 'The code is entered incorrectly!'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                refresh = RefreshToken.for_user(user)
                access_token =  str(refresh.access_token)
                return Response({
                    'message': 'Code entered correctly!',
                    "access_token": access_token,
                    "refresh_token": str(refresh)
                }, status=status.HTTP_200_OK)
            

class PasswordRecoveryChangeView(generics.UpdateAPIView):
    serializer_class = serializers.PasswordRecoveryChange
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        data = request.data
        user = request.user

        if len(data['new_password']) < 8:
            return Response({"message": "Password shorter than 8 characters"}, status=status.HTTP_400_BAD_REQUEST)
        if data['new_password'] != data['confirm_new_password']:
            return Response({"message": "New password fields do not match!"}, status=status.HTTP_400_BAD_REQUEST)
        new_password = data['new_password']
        user.set_password(new_password)
        user.save()
        profile = models.Profiles.objects.get(user_id=user.id)
        profile.updated = datetime.now()
        profile.save()
        return Response({"message": "Password updated succesfully!"}, status=status.HTTP_200_OK)
