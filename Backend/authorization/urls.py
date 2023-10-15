from cmath import log
from django.urls import path
from authorization import views

urlpatterns = [
    path("registration", views.RegisterView.as_view()),
    path("login", views.login_view),
    path("change-password/", views.ChangePasswordView.as_view()),
    path("token-refresh", views.RefreshTokenView.as_view(), name='token_refresh'),
    path('password-recovery-request', views.password_recovery_request_view),
    path('password-recovery-change', views.PasswordRecoveryChangeView.as_view(), name='password-recovery-change'),
    path('logout', views.Logout_View.as_view(), name='auth_logout')
]
