from django.urls import path
from ai_recipes import views

urlpatterns = [
    path("suggestions", views.AIRecipesView.as_view()),
]
