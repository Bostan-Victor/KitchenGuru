from django.urls import path
from filtering_test import views

urlpatterns = [
    path("list", views.FilteringView.as_view()),
]
