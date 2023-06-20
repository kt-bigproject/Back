from django.urls import path, include, re_path
from rest_auth.views import LoginView, LogoutView, PasswordChangeView
from rest_auth.registration.views import VerifyEmailView, RegisterView
from . import views
from sign.views import ConfirmEmailView


urlpatterns = [
    # 로그인
    path('login/', LoginView.as_view(), name='rest_login'),
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    path('password/change/', PasswordChangeView.as_view(), name='rest_password_change'),

    # 회원가입
    path('registration/', RegisterView.as_view(), name='rest_register'),
    path('naver/', views.NaverLogin.as_view(), name='naver'),
    path('naver/login/', views.naver_login, name='naver_login'),
    path('naver/callback/', views.naver_callback, name='naver_callback'),
    path('naver/login/finish/', views.NaverLogin.as_view(), name='naver_login_todjango'),

    # 유효한 이메일이 유저에게 전달
    re_path(r'^account-confirm-email/$', VerifyEmailView.as_view(), name='account_email_verification_sent'),

    # 유저가 클릭한 이메일(=링크) 확인
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(), name='account_confirm_email'),
    
]