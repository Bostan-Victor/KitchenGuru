from rest_framework import serializers, status
from users import models
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
import logging
import logging.config

logging.config.fileConfig(r'C:\Users\PС\Desktop\KG\KitchenGuru\Backend\KitchenGuru\system_activity.conf', disable_existing_loggers=False)

SYSTEM_LOGGER = logging.getLogger('activity')


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=32, write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attr):
        username_exist = models.Users.objects.filter(username=attr['username']).exists()
        email_exist = models.Users.objects.filter(email=attr['email']).exists()
        if username_exist:
            SYSTEM_LOGGER.warning(f"Registration attempt with existing username: {attr['username']}")
            raise serializers.ValidationError("Username is already in use")
        if email_exist:
            SYSTEM_LOGGER.warning(f"Registration attempt with existing email: {attr['email']}")
            raise serializers.ValidationError("Email is already in use")
        if len(attr['password']) < 8:
            raise serializers.ValidationError("Password is shorter than 8 characters!")
        if attr['password'] != attr['confirm_password']:
            raise serializers.ValidationError("Password fields do not match!")
        return attr
    
    def create(self, validated_data):
        confirm_password = validated_data.pop("confirm_password")
        validated_data['password'] = make_password(validated_data['password'])
        user = models.Users.objects.create(**validated_data)
        profile = models.Profiles.objects.create(user=user)
        rec_code = models.PasswordRecovery.objects.create(user=user)
        token_object = models.Tokens.objects.create(user=user)

        SYSTEM_LOGGER.info(f"New user registered with username: {validated_data['username']}")
        return user
    

class LoginSerializer(serializers.Serializer):
    username_email = serializers.CharField(max_length=32)
    password = serializers.CharField(max_length=32)


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=32)
    new_password = serializers.CharField(max_length=32)
    confirm_new_password = serializers.CharField(max_length=32)

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return self.update(request, *args, **kwargs)
    

class PasswordRecoveryRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class SendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    link = serializers.CharField(max_length=255)


class PasswordRecoveryChange(serializers.Serializer):
    new_password = serializers.CharField(max_length=32)
    confirm_new_password = serializers.CharField(max_length=32)

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return self.update(request, *args, **kwargs)

class LogOut(serializers.Serializer):
    user_id = serializers.IntegerField()