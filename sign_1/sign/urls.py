from django.urls import path, include, re_path
from django.contrib import admin
from django.views.generic import TemplateView
from rest_auth.views import LoginView, LogoutView, PasswordChangeView
from rest_auth.registration.views import VerifyEmailView, RegisterView
from sign.views import ConfirmEmailView

urlpatterns = [
    path("admin/", admin.site.urls),
    # allauth
    path('accounts/', include('allauth.urls')),
    path('', include('predict.urls')),
    # 로그인
    path('rest-auth/login/', LoginView.as_view(), name='rest_login'),
    path('rest-auth/logout/', LogoutView.as_view(), name='rest_logout'),
    path('rest-auth/password/change/', PasswordChangeView.as_view(), name='rest_password_change'),

    # 회원가입
    path('rest-auth/registration/', RegisterView.as_view(), name='rest_register'),

    # 이메일 관련 필요
    path('accounts/allauth/', include('allauth.urls')),

    # 유효한 이메일이 유저에게 전달
    re_path(r'^account-confirm-email/$', VerifyEmailView.as_view(), name='account_email_verification_sent'),

    # 유저가 클릭한 이메일(=링크) 확인
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(), name='account_confirm_email'),

]
