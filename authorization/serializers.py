from rest_framework import serializers
from users import models


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField()
    class Meta:
        model = models.Users
        fields = ["username", "email", "password", "confirm_password"]

    def validate(self, attr):
        if attr['password'] != attr['confirm_password']:
            raise serializers.ValidationError("Password fields do not match!")
        return attr
    
    def create(self, validated_data):
        return models.Users.objects.create(
            username=validated_data['username'], 
            email=validated_data['email'],
            password=validated_data['password'])
    
