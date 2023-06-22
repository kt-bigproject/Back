# api/urls.py
from django.urls import path, re_path
from . import views
from rest_auth.views import PasswordChangeView
from .views import email_verification_view, KakaoSignView, KakaoCallBackView
from .views import  google_login, google_callback, GoogleLogin
from .views import NaverLoginAPIView, NaverCallbackAPIView, NaverLoginView

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

    path('password/change/', PasswordChangeView.as_view(), name='rest_password_change'),
    path('', views.getRoutes),

    # google 로그인
    path('google/login/', google_login, name='google_login'),
    path('google/callback/', google_callback, name='google_callback'),
    path('google/login/finish/', GoogleLogin.as_view(), name='google_login_todjango'),
    # naver 로그인
    path('naver/login/', NaverLoginAPIView.as_view()),
    path('naver/callback/', NaverCallbackAPIView.as_view()),
    path('naver/login/finish/', NaverLoginView.as_view()),
    # kakao 로그인
    path('kakao/login/', KakaoSignView.as_view(), name='kakao_login'),
    path('kakao/callback/', KakaoCallBackView.as_view(), name='kakao_callback'),
    path('kakao/login/finish/', views.KakaoLogin.as_view(), name='kakao_login_todjango'),

]
