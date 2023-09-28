from django.urls import path
from recipes import views


urlpatterns = [
    path('create-recipe', views.CreateRecipeView.as_view()),
    path('recipe-review', views.CreateReviewView.as_view())
    # path('get-recipes', views.GetRecipes.as_view())
]