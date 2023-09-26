from django.contrib import admin
from recipes.models import Review
# Register your models here.

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'review', 'rating', 'date', 'text')
    
    
admin.site.register(Review)