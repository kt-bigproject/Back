import requests
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.naver import views as naver_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from sign.models import User
from django.shortcuts import redirect
from django.conf import settings
from json.decoder import JSONDecodeError
from allauth.socialaccount.models import SocialAccount
from django.http import JsonResponse



BASE_URL = 'http://localhost:8000/rest-auth/'
NAVER_CALLBACK_URI = BASE_URL + 'naver/callback/'

def naver_login(request):
    rest_api_key = getattr(settings, 'NAVER_REST_API_KEY')
    return redirect(
        f"https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={rest_api_key}&redirect_uri={NAVER_CALLBACK_URI}&state=LOGIN"
    )
def naver_callback(request):
    rest_api_key = getattr(settings, 'NAVER_REST_API_KEY')
    code = request.GET.get("code")
    redirect_uri = NAVER_CALLBACK_URI
    """
    Access Token Request
    """
    token_req = requests.get(
        f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={rest_api_key}&redirect_uri={redirect_uri}&code={code}")
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get("access_token")
    """
    Email Request
    """
    profile_request = requests.get(
        "https://openapi.naver.com/v1/nid/me", headers={"Authorization": f"Bearer {access_token}"})
    profile_json = profile_request.json()
    naver_account = profile_json.get('naver_account')
    # print(naver_account)
    email = naver_account.get('email')
    """
    Signup or Signin Request
    """
    try:
        user = User.objects.get(email=email)
        # 기존에 가입된 유저의 Provider가 naver가 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        if social_user.provider != 'naver':
            return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
        # 기존에 Google로 가입된 유저
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}accounts/naver/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json)
    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}accounts/naver/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
        # user의 pk, email, first name, last name과 Access Token, Refresh token 가져옴
        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json)
    
class NaverLogin(SocialLoginView):
    adapter_class = naver_view.NaverOAuth2Adapter
    callback_url = NAVER_CALLBACK_URI
    client_class = OAuth2Client


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


