from django.urls import path
from recipes import views


urlpatterns = [
    path('create-recipe', views.CreateRecipeView.as_view())
]