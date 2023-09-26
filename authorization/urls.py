from django.urls import path
from authorization import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

urlpatterns = [
    path("registration", views.RegisterView.as_view()),
    path("login", views.login_view),
    path("change-password/", views.ChangePasswordView.as_view()),
    path("token", TokenObtainPairView.as_view(), name= 'token_obtain_pair'),
    path("token/refresh", TokenRefreshView.as_view(), name='token_refresh'),
    path('password-recovery-request', views.password_recovery_request_view),
    path('password-recovery-confirm', views.password_recovery_confirm_view),
    path('password-recovery-change', views.PasswordRecoveryChangeView.as_view())
]
