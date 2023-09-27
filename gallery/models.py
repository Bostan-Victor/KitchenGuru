# from users import models
from django.db import models

# Create your models here.
class Image(models.Model):
    title = models.CharField(max_length=32)
    image = models.ImageField(upload_to='images')
    
    def __str__(self):
        return self.title