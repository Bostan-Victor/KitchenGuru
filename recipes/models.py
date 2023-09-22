from django.db import models

class Recipes(models.Model):
    title = models.CharField(max_length=255, null=False)
    ingredients = models.TextField(null=False)
    instructions = models.TextField(null=False)
    image_name = models.ImageField(upload_to="static/recipes", default="static/recipes/no_recipe.jpg")
