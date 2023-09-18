from django.urls import path
from superuser import views

urlpatterns = [
    path("profiles", views.ProfileView.as_view())

]
