from rest_framework import serializers
from users import models
from django.contrib.auth.hashers import make_password


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField()
    class Meta:
        model = models.Users
        fields = ["username", "email", "password", "confirm_password"]

    def validate(self, attr):
        if len(attr['password']) < 8:
            raise serializers.ValidationError("Password is shorter than 8 characters!")
        if attr['password'] != attr['confirm_password']:
            raise serializers.ValidationError("Password fields do not match!")
        return attr
    
    def create(self, validated_data):
        return models.Users.objects.create(
            username=validated_data['username'], 
            email=validated_data['email'],
            password=make_password(validated_data['password']))
    

class LoginSerializer(serializers.ModelSerializer):
    username2 = serializers.CharField()
    password2 = serializers.CharField()
    class Meta:
        model = models.Users
        fields = ["username", "password"]

    def validate(self, attr):
        if attr['username2'] == attr['username'] and attr['password2'] == attr['password']:
            return attr
  