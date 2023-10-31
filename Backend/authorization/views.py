from http.client import HTTPResponse
from tokenize import Token
from urllib import response
from urllib.request import Request
from rest_framework import generics, status
from authorization import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from users import models
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt import views
from django.core.mail import send_mail
from django.core.signing import Signer
from datetime import datetime, timedelta
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import logout
from random import randint
import logging
import logging.config
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, '..', 'KitchenGuru', 'user_activity.conf')
logging.config.fileConfig(config_path, disable_existing_loggers=False)
USER_LOGGER = logging.getLogger('user')
config_path = os.path.join(current_dir, '..', 'KitchenGuru', 'system_activity.conf')
logging.config.fileConfig(config_path, disable_existing_loggers=False)
SYSTEM_LOGGER = logging.getLogger('activity')


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
            USER_LOGGER.warning(f"User Agent {request.META.get('HTTP_USER_AGENT')} failed to log in with username/email {data['username_email']} from remote address {request.META.get('REMOTE_ADDR')}")
            SYSTEM_LOGGER.warning(f"Failed login attempt with username or email: {data['username_email']}, User agent: {request.META.get('HTTP_USER_AGENT')}, from remote address {request.META.get('REMOTE_ADDR')}")
            return Response({"message": "Username or Email invalid!"}, status=status.HTTP_404_NOT_FOUND)
    try:
        profile = models.Profiles.objects.get(user_id=user.id)
        profile.last_login = datetime.now()
        profile.save()
    except models.Profiles.DoesNotExist:
        SYSTEM_LOGGER.warning(f"User with username or email: {data['username_email']} has no profile created, User agent: {request.META.get('HTTP_USER_AGENT')}, from remote address {request.META.get('REMOTE_ADDR')}")
        return Response({"message": "Profile does not exist!"}, status=status.HTTP_404_NOT_FOUND)
    # token, created = models.Tokens.objects.get_or_create()
    if check_password(data['password'], user.password):
        refresh = RefreshToken.for_user(user)
        access_token =  str(refresh.access_token)
        token_object = models.Tokens.objects.get(user_id=user.id)
        token_object.access_token = access_token
        token_object.refresh_token = str(refresh)
        token_object.save()
        
        if user.is_superuser:
            return Response({"message": "Admin logged in",
                             "access_token": access_token,
                             "refresh_token": str(refresh)}, status=status.HTTP_200_OK)
        else:
            USER_LOGGER.info(f"User {user.username}, User Agent {request.META.get('HTTP_USER_AGENT')} successfully logged in from remote address {request.META.get('REMOTE_ADDR')}")
            return Response({"message": "User logged in!",
                    "access_token": access_token,
                    "refresh_token": str(refresh) }, status=status.HTTP_200_OK)
    else:
        USER_LOGGER.warning(f"User Agent {request.META.get('HTTP_USER_AGENT')} failed to log in with incorrect password from remote address {request.META.get('REMOTE_ADDR')}")
    return Response({"message": "Password invalid!"}, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def update(self, request):
        user_id = request.user.id
        try:
            user_tokens = models.Tokens.objects.get(user_id=user_id)
            USER_LOGGER.info(f"User '{request.user.username}', User Agent {request.META.get('HTTP_USER_AGENT')} refreshed token from remote address {request.META.get('REMOTE_ADDR')}")
        except:
            SYSTEM_LOGGER.error(f"Failed to get tokens for user ID: {user_id}")
            return Response({'message': 'The provided access token is invalid!'}, status=status.HTTP_401_UNAUTHORIZED)
        refresh_token = RefreshToken(user_tokens.refresh_token)
        new_access_token = str(refresh_token.access_token)
        user_tokens.access_token = new_access_token
        user_tokens.save()
        return Response({'access_token': new_access_token}, status=status.HTTP_200_OK)


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
            USER_LOGGER.info(f"User '{user.username}' changed password, User Agent {request.META.get('HTTP_USER_AGENT')} from remote address {request.META.get('REMOTE_ADDR')}")
            profile = models.Profiles.objects.get(user_id=user.id)
            profile.updated = datetime.now()
            profile.save()
            SYSTEM_LOGGER.info(f"User {user.id} changed password successfully.")
            return Response({"message": "Password updated succesfully!"}, status=status.HTTP_200_OK)
        else:
            SYSTEM_LOGGER.warning(f"User {user.id} failed to change password due to incorrect old password.")
            return Response({"message": "Old password is incorrect!"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def password_recovery_request_view(request):
    data = request.data
    serializer = serializers.PasswordRecoveryRequestSerializer(data=data)
    serializer.is_valid(raise_exception=True)

    try:
        models.Users.objects.get(email=data['email'])
        random_code = str(randint(100000, 999999))
        USER_LOGGER.info(f"Password recovery requested for email '{data['email']}', User Agent {request.META.get('HTTP_USER_AGENT')} from remote address {request.META.get('REMOTE_ADDR')}")
        return Response({'code': random_code}, status=status.HTTP_200_OK)
    except models.Users.DoesNotExist:
        SYSTEM_LOGGER.warning(f"Password recovery request for invalid email: {data['email']}")
        return Response({'message': 'This email is not valid!'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['POST'])
def send_email_view(request):
    data = request.data
    serializer = serializers.SendEmailSerializer(data=data)
    serializer.is_valid(raise_exception=True)

    send_mail(
        'KitchenGuru - Password Recovery',
        f'Click this link to change your password:\n{data["link"]}',
        'KitchenGuru@mail.com',
        [data['email']],
        fail_silently=False
    )
    USER_LOGGER.info(f"Password recovery email sent to '{data['email']}', User Agent {request.META.get('HTTP_USER_AGENT')} from remote address {request.META.get('REMOTE_ADDR')}")

    user = models.Users.objects.get(email=data['email'])
    pass_recovery_object = models.PasswordRecovery.objects.get(user_id=user.id)
    pass_recovery_object.created_at = datetime.now()
    pass_recovery_object.is_used = False
    pass_recovery_object.save()
    SYSTEM_LOGGER.info(f"Password recovery email sent to: {data['email']}")
    return Response({'message': 'Email sent successfully!'}, status=status.HTTP_200_OK)
            

class PasswordRecoveryChangeView(generics.UpdateAPIView):
    serializer_class = serializers.PasswordRecoveryChange

    def update(self, request, *args, **kwargs):
        data = request.data
        email = request.query_params.get('email')
        user = models.Users.objects.get(email=email)
        pass_recovery_object = models.PasswordRecovery.objects.get(user_id=user.id)
        created_at = pass_recovery_object.created_at
        now = timezone.now()
        delta = timedelta(minutes=15)

        if pass_recovery_object.is_used:
            return Response({"message": "The link has been used already!"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            if now - created_at > delta:
                return Response({"message": "The link has expired!"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                if len(data['new_password']) < 8:
                    return Response({"message": "Password shorter than 8 characters"}, status=status.HTTP_400_BAD_REQUEST)
                if data['new_password'] != data['confirm_new_password']:
                    return Response({"message": "New password fields do not match!"}, status=status.HTTP_400_BAD_REQUEST)
                new_password = data['new_password']
                user.set_password(new_password)
                user.save()
                USER_LOGGER.info(f"User '{user.username}' changed password through recovery link, User Agent {request.META.get('HTTP_USER_AGENT')} from remote address {request.META.get('REMOTE_ADDR')}")
                profile = models.Profiles.objects.get(user_id=user.id)
                profile.updated = datetime.now()
                profile.save()
                pass_recovery_object.is_used = True
                pass_recovery_object.save()
                SYSTEM_LOGGER.info(f"Password changed through recovery for email: {email}")
                return Response({"message": "Password updated succesfully!"}, status=status.HTTP_200_OK)


class Logout_View(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_id = request.user.id

        try: 
            token = models.Tokens.objects.get(user_id=user_id)
        except models.Tokens.DoesNotExist:  
            return Response({"message": f"For user {request.user} could not find any tokens"},
                            status=status.HTTP_401_UNAUTHORIZED)

        token.access_token = None
        token.refresh_token = None
        token.save()
        USER_LOGGER.info(f"User '{request.user.username}' logged out, User Agent {request.META.get('HTTP_USER_AGENT')} from remote address {request.META.get('REMOTE_ADDR')}")
        SYSTEM_LOGGER.info(f"User with ID {user_id} logged out successfully.")
        return Response({"message": "User logged out succesfully!"})
        