from django.urls import path
from authorization import views

urlpatterns = [
    path("registration", views.RegisterView.as_view()),
    path("login", views.login_view),
    path("change_password", views.change_password_view)
]
