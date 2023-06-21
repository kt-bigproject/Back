#api/views.py
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from api.serializer import MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from rest_framework.views import APIView

# Create your views here.
def email_verification_view(request):
    uidb64 = request.GET.get('uid')
    token = request.GET.get('token')

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        # 처리할 수 없는 사용자 ID이거나 사용자가 존재하지 않을 경우 예외 처리
        return redirect('email-verification-failed')  # 실패 페이지로 이동하거나 적절한 에러 처리

    if default_token_generator.check_token(user, token):
        # 토큰이 유효한 경우 사용자 계정 활성화
        user.is_active = True
        user.save()
        return redirect('email-verification-success')  # 성공 페이지로 이동하거나 적절한 응답 반환
    else:
        # 토큰이 유효하지 않은 경우 실패 처리
        return redirect('email-verification-failed')  # 실패 페이지로 이동하거나 적절한 에러 처리

def email_verification_success(request):
    return render(request, 'email_verification_success.html')

def email_verification_failed(request):
    return render(request, 'email_verification_failed.html')


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        # 성공 시나리오는 React Router Route가 처리할 것입니다.
        return Response({'message': 'Email confirmed successfully.'})

    def get_object(self):
        key = self.kwargs['key']
        email_confirmation = EmailConfirmationHMAC.from_key(key)
        if not email_confirmation:
            raise NotFound('Email confirmation not found.')
        return email_confirmation

    def get_queryset(self):
        qs = EmailConfirmation.objects.all_valid()
        qs = qs.select_related("email_address__user")
        return qs


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token/',
        '/api/register/',
        '/api/token/refresh/'
    ]
    return Response(routes)