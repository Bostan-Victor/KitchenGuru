from rest_framework import serializers, status
from users import models
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from rest_framework.response import Response


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
        try:
            user = models.Users.objects.create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError({"message": "Username or email already exists."})
                # return Response({"message": "An error occured"}, status=status.HTTP_401_UNAUTHORIZED)
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
  