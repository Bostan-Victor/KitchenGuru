from unittest.util import _MAX_LENGTH
from django.db import models
from users.models import Users


class Recipes(models.Model):
    CATEGORY_CHOICES = (
        ('soups', 'Soups'),
        ('salad', 'Salads'),
        ('seafood', 'Sea Food'),
        ('desserts', 'Desserts'),
        ('fast_food', 'Fast Food'),
        ('meat', 'Meat')
    )

    title = models.CharField(max_length=255, null=False)
    ingredients = models.TextField(null=False)
    instructions = models.TextField(null=False)
    category = models.CharField(max_length=10, null=True, choices=CATEGORY_CHOICES)
    duration = models.IntegerField(null=True)
    ingredient_tags = models.CharField(max_length=255, null=True)
    created_by = models.ForeignKey(Users, null=True, on_delete=models.CASCADE)


class AIRecipes(models.Model):
    message = models.TextField()
    image_url = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Users, on_delete=models.CASCADE)


class Ingredients(models.Model):
    name = models.CharField(max_length=255)


class RecipesImages(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="recipes/", default="static/recipes/no_recipe.jpg", max_length=500)


class Favorites(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)


class Review(models.Model):
    recipes = models.ForeignKey(Recipes, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(Users, verbose_name="User", on_delete=models.CASCADE)
    rating = models.IntegerField(null=True)
    text = models.TextField(max_length=255)
    review_date = models.DateTimeField(null=True)
