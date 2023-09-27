from django.db import models
from users.models import Users

class Recipes(models.Model):
    title = models.CharField(max_length=255, null=False)
    ingredients = models.TextField(null=False)
    instructions = models.TextField(null=False)
    image_name = models.ImageField(upload_to="static/recipes", default="static/recipes/no_recipe.jpg")


class Review(models.Model):
    recipes = models.ForeignKey(Recipes, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(Users, verbose_name="User", on_delete=models.CASCADE)
    rating = models.IntegerField(null=True)
    text = models.TextField(max_length=255)
    review_added = models.DateTimeField(null=True)
    