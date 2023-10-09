from django.urls import path
from recipes import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('create-recipe', views.CreateRecipeView.as_view()),
    path('recipe-review', views.CreateReviewView.as_view()),
    path('get-recipes', views.GetRecipes.as_view()),
    path('get-ingredients', views.GetIngredients.as_view()),
    path('best100', views.FilteringView.as_view()),
    path('search', views.SearchRecipesView.as_view()),
    path('filter', views.FilterRecipesView.as_view())
] 
