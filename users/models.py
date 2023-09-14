from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = None
    last_name = None
    user_permissions = None
    groups = None


class Profiles(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    avatar = models.ImageField(upload_to="static/avatars", default="static/avatars/no_picture.png")
    last_login = models.DateTimeField()
    updated = models.DateTimeField()
      
