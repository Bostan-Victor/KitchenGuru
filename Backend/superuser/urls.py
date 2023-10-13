from django.urls import path
from superuser import views

urlpatterns = [
    path("profile", views.AdminView.as_view())
]
