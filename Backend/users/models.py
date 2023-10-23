from django.db import models
from django.contrib.auth.models import AbstractUser



class Users(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = None
    last_name = None
    user_permissions = None
    groups = None


class Profiles(models.Model):
    user = models.OneToOneField(
        Users,
        on_delete=models.CASCADE,
        primary_key=True
    )
    first_name = models.CharField(max_length=32, null=True)
    last_name = models.CharField(max_length=32, null=True)
    avatar = models.ImageField(upload_to="avatars", default="static/avatars/no_picture.png")
    last_login = models.DateTimeField(null=True)
    updated = models.DateTimeField(null=True)


class PasswordRecovery(models.Model):
    user = models.OneToOneField(
        Users,
        on_delete=models.CASCADE,
        primary_key=True
    )
    created_at = models.DateTimeField(null=True)
    is_used = models.BooleanField(default=False)


class Tokens(models.Model):
    user = models.OneToOneField(
        Users, 
        on_delete=models.CASCADE,
        primary_key=True
    )
    access_token = models.CharField(max_length=255, null=True)
    refresh_token = models.CharField(max_length=255, null=True)


class WatchList(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    recipe = models.ForeignKey('recipes.Recipes', on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)