from django.urls import path
from recipes import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('create-recipe', views.CreateRecipeView.as_view()),
    path('recipe-review', views.CreateReviewView.as_view()),
    path('get-recipes', views.GetRecipes.as_view()),
    path('get-ingredients', views.GetIngredients.as_view()),
    path('add-favorites', views.AddFavorites.as_view())
] 
