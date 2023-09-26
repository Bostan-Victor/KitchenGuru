from django.db import models

class TestRecipes(models.Model):
    title = models.CharField(max_length=64, null=True)
    comment_count = models.IntegerField(null=True)
    rating = models.FloatField(null=True)
    ingredients = models.CharField(null=True)
    instructions = models.CharField(null=True)
    category = models.CharField(max_length=64, null=True)
    favorites_count = models.IntegerField(null=True)
    duration_time = models.IntegerField(null=True)


