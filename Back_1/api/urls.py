# api/urls.py
from django.urls import path, re_path
from . import views
from rest_auth.views import LoginView, LogoutView, PasswordChangeView
from rest_auth.registration.views import VerifyEmailView, RegisterView
from .views import ConfirmEmailView
from .views import email_verification_view

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('email-verification/', email_verification_view, name='email-verification'),
    path('email-verification-success/', views.email_verification_success, name='email-verification-success'),
    path('email-verification-failed/', views.email_verification_failed, name='email-verification-failed'),
    
    path('login/', LoginView.as_view(), name='rest_login'),
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    path('password/change/', PasswordChangeView.as_view(), name='rest_password_change'),
    path('', views.getRoutes),
]
