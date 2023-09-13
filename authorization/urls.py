from django.urls import path
from authorization import views

urlpatterns = [
    path("registration", views.RegisterView.as_view())
]
