from rest_framework import serializers
from users import models
from django.contrib.auth.hashers import make_password


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=32, write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attr):
        if len(attr['password']) < 8:
            raise serializers.ValidationError("Password is shorter than 8 characters!")
        if attr['password'] != attr['confirm_password']:
            raise serializers.ValidationError("Password fields do not match!")
        return attr
    
    def create(self, validated_data):
        confirm_password = validated_data.pop("confirm_password")
        validated_data['password'] = make_password(validated_data['password'])
        user = models.Users.objects.create(**validated_data)
        return user
    

class LoginSerializer(serializers.Serializer):
    username_email = serializers.CharField(max_length=32)
    password = serializers.CharField(max_length=32)


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=32)
    new_password = serializers.CharField(max_length=32)
    confirm_new_password = serializers.CharField(max_length=32)
  