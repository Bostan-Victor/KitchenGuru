from django.db import models


class Users(models.Model):
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class Profiles(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    avatar = models.ImageField(upload_to="static/avatars", default="static/avatars/no_picture.png")
    last_login = models.DateTimeField()
    updated = models.DateTimeField()
      
