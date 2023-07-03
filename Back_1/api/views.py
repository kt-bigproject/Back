#api/views.py
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from api.serializer import MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.naver import views as naver_views
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from ogle import settings
import requests
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from dj_rest_auth.registration.views import SocialLoginView
from json.decoder import JSONDecodeError
from allauth.socialaccount.models import SocialAccount
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.providers.kakao import views as kakao_views
from api.models import UserProfile
import rest_framework_simplejwt as jwt
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.http import HttpResponseRedirect

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


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token/',
        '/api/register/',
        '/api/token/refresh/'
    ]
    return Response(routes)


from django.contrib.auth import get_user_model

User = get_user_model()

BASE_URL = 'http://localhost:8000/'
FRONT_URL = 'http://localhost:3000/'
GOOGLE_CALLBACK_URI = BASE_URL + 'api/google/callback/'
NAVER_CALLBACK_URI = BASE_URL + 'api/naver/callback/'

def create_user_with_token(request):
    # 사용자 생성 로직...

    # JWT 토큰 생성
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    # 응답에 토큰 포함하여 반환
    return Response({"access_token": access_token})

def google_login(request):
    """
    Code Request
    """
    scope = "https://www.googleapis.com/auth/userinfo.email"
    client_id = settings.SOCIAL_AUTH_GOOGLE_CLIENT_ID
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")


def google_callback(request):
    client_id = settings.SOCIAL_AUTH_GOOGLE_CLIENT_ID
    client_secret = settings.SOCIAL_AUTH_GOOGLE_SECRET
    code = request.GET.get('code')

    """
    Access Token Request
    """
    token_req = requests.post(
        f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={settings.STATE}")
    token_req_json = token_req.json()
    error = token_req_json.get("error")

    if error is not None:
        raise JSONDecodeError(error)
    
    access_token = token_req_json.get('access_token')
    """
    Email Request
    """
    email_req = requests.get(
        f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
    email_req_status = email_req.status_code

    if email_req_status != 200:
        return JsonResponse({'err_msg1': 'failed to get email'}, status=statistics.HTTP_400_BAD_REQUEST)
    
    email_req_json = email_req.json()
    email = email_req_json.get('email')

    """
    Signup or Signin Request
    """
    try:
        user = User.objects.get(email=email)
        # 기존에 가입된 유저의 Provider가 google이 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        if social_user.provider != 'google':
            return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
        # 기존에 Google로 가입된 유저
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}api/google/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg2': 'failed to signin'}, status=accept_status)

        token = AccessToken.for_user(user)

            # 기타 필요한 정보 추가
        token['username'] = user.username
        token['email'] = user.email

        refresh = RefreshToken.for_user(user)  # refresh_token 발급

        accept_json = accept.json()
        accept_json.pop('user', None)            # 프로필 정보 업데이트


        # return JsonResponse({
        #     "token": str(token),
        #     "refresh_token": str(refresh),
        # }, status=200)
        
        response = HttpResponseRedirect(FRONT_URL)
        response.set_cookie('token', str(token))
        response.set_cookie('refresh_token', str(refresh))
        
        return response

    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}api/google/login/finish/", data=data)
        accept_status = accept.status_code
   #     print(access_token)
    #    print('-'*50)
     #   print(code)
        if accept_status != 200:
            return JsonResponse({'err_msg3': 'failed to signup'}, status=accept_status)
        
        accept_json = accept.json()
        accept_json.pop('user', None)

        user = User.objects.get(email=email)
        
        token = AccessToken.for_user(user)

            # 기타 필요한 정보 추가
        token['username'] = user.username
        token['email'] = user.email

        refresh = RefreshToken.for_user(user)  # refresh_token 발급

        # return JsonResponse({
        #     "token": str(token) ,
        #     "refresh_token": str(refresh),
        # }, status=200)
        response = HttpResponseRedirect(FRONT_URL)
        response.set_cookie('token', str(token))
        response.set_cookie('refresh_token', str(refresh))
        
        return response

    
    except SocialAccount.DoesNotExist:
    	# User는 있는데 SocialAccount가 없을 때 (=일반회원으로 가입된 이메일일때)
        return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)

class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client

class NaverLoginAPIView(APIView):
    # 로그인을 위한 창은 누구든 접속이 가능해야 하기 때문에 permission을 AllowAny로 설정
    permission_classes = (AllowAny,)
    
    def get(self, request, *args, **kwargs):
        client_id = settings.NAVER_CLIENT_ID
        response_type = "code"
        # Naver에서 설정했던 callback url을 입력해주어야 한다.
        uri = BASE_URL + "/api/naver/callback"
        state = settings.STATE
        # Naver Document 에서 확인했던 요청 url
        url = "https://nid.naver.com/oauth2.0/authorize"
        
        # Document에 나와있는 요소들을 담아서 요청한다.
        return redirect(
            f'{url}?response_type={response_type}&client_id={client_id}&redirect_uri={uri}&state={state}'
        )


class NaverCallbackAPIView(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request, *args, **kwargs):
        try:
            # Naver Login Parameters
            grant_type = 'authorization_code'
            client_id = settings.NAVER_CLIENT_ID
            client_secret = settings.NAVER_CLIENT_SECRET
            code = request.GET.get('code')
            state = request.GET.get('state')

            parameters = f"grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}&code={code}&state={state}"

            # token request
            token_request = requests.get(
                f"https://nid.naver.com/oauth2.0/token?{parameters}"
            )

            token_response_json = token_request.json()
            error = token_response_json.get("error", None)

            if error is not None:
                raise JSONDecodeError(error)

            access_token = token_response_json.get("access_token")

            # User info get request
            user_info_request = requests.get(
                "https://openapi.naver.com/v1/nid/me",
                headers={"Authorization": f"Bearer {access_token}"},
            )

            # User 정보를 가지고 오는 요청이 잘못된 경우
            if user_info_request.status_code != 200:
                return JsonResponse({"error": "failed to get email."}, status=status.HTTP_400_BAD_REQUEST)

            user_info = user_info_request.json().get("response")
            email = user_info["email"]

            # User 의 email 을 받아오지 못한 경우
            if email is None:
                return JsonResponse({
                    "error": "Can't Get Email Information from Naver"
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                # data = {'access_token': access_token, 'code': code}
                # # accept 에는 token 값이 json 형태로 들어온다({"key"}:"token value")
                # # 여기서 오는 key 값은 authtoken_token에 저장된다.
                # accept = requests.post(
                #     f"{BASE_URL}api/naver/login/finish", data=data
                # )
                # # 만약 token 요청이 제대로 이루어지지 않으면 오류처리
                # if accept.status_code != 200:
                #     return JsonResponse({"error": "Failed to Signin."}, status=accept.status_code)
                # return Response(accept.json(), status=status.HTTP_200_OK)
            
                user = User.objects.get(email=email)
                # 기존에 가입된 유저의 Provider가 naver이 아니면 에러 발생, 맞으면 로그인
                # 다른 SNS로 가입된 유저
                social_user = SocialAccount.objects.get(user=user)
                if social_user is None:
                    return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
                if social_user.provider != 'naver':
                    return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
                # 기존에 Naver로 가입된 유저
                data = {'access_token': access_token, 'code': code}
                accept = requests.post(
                    f"{BASE_URL}api/naver/login/finish/", data=data
                )
                accept_status = accept.status_code
                if accept_status != 200:
                    return JsonResponse({'err_msg2': 'failed to signin'}, status=accept_status)

                token = AccessToken.for_user(user)

                    # 기타 필요한 정보 추가
                token['username'] = user.username
                token['email'] = user.email

                refresh = RefreshToken.for_user(user)  # refresh_token 발급

                accept_json = accept.json()
                accept_json.pop('user', None)            # 프로필 정보 업데이트

                response = HttpResponseRedirect(FRONT_URL)
                response.set_cookie('token', str(token))
                response.set_cookie('refresh_token', str(refresh))
                
                return response
                # return JsonResponse({
                #     "token": str(token),
                #     "refresh_token": str(refresh),
                # }, status=200)
                # accept_json = accept.json()
                # accept_json.pop('user', None)
                # return JsonResponse(accept_json)

            except User.DoesNotExist:

                data = {'access_token': access_token, 'code': code}
                accept = requests.post(
                    f"{BASE_URL}api/naver/login/finish/", data=data
                )
                accept_json = accept.json()
                accept_json.pop('user', None)

                user = User.objects.get(email=email)
                
                token = AccessToken.for_user(user)

                    # 기타 필요한 정보 추가
                token['username'] = user.username
                token['email'] = user.email

                refresh = RefreshToken.for_user(user)  # refresh_token 발급

                response = HttpResponseRedirect(FRONT_URL)
                response.set_cookie('token', str(token))
                response.set_cookie('refresh_token', str(refresh))
                
                return response
                # return JsonResponse({
                #     "token": str(token) ,
                #     "refresh_token": str(refresh),
                # }, status=200)
                # print(access_token)
                # print("----------------------------")
                # print(code)
                # return Response(accept.json(), status=status.HTTP_200_OK)
                
        except:
            return JsonResponse({
                "error": "error",
            }, status=status.HTTP_404_NOT_FOUND)
            
   
class NaverLoginView(SocialLoginView):
    adapter_class = naver_views.NaverOAuth2Adapter
    callback_url = NAVER_CALLBACK_URI
    client_class = OAuth2Client
    
    def get_response_data(self, sociallogin):
        # 원래 get_response_data() 메서드의 동작을 수행합니다.
        response = super().get_response_data(sociallogin)

        # 사용자 정보 가져오기
        user = sociallogin.user

        # JWT 토큰 생성
        refresh = RefreshToken.for_user(user)
        token = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        print(token['refresh'])
        print("----------------------------")
        print(token['access'])
        # 응답 데이터에 JWT 토큰 추가
        response['token'] = token

        return response

KAKAO_CALLBACK_URI = BASE_URL + 'api/kakao/callback/'
class KakaoSignView(View):
    def get(self, request):
        rest_api_key = settings.KAKAO_REST_API_KEY
        redirect_uri = KAKAO_CALLBACK_URI
        authorization_url = f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={redirect_uri}&response_type=code&scope=&scope=account_email,profile_nickname,profile_image"
        return redirect(authorization_url)

class KakaoException(Exception):
    pass

class KakaoCallBackView(APIView):
    def get(self, request):
        auth_code = request.GET.get('code')
        kakao_token_api = 'https://kauth.kakao.com/oauth/token'

        data = {
            'grant_type': 'authorization_code',
            'client_id': settings.KAKAO_REST_API_KEY,
            'redirect_uri': KAKAO_CALLBACK_URI,
            'code': auth_code,
        }

        token_response = requests.post(kakao_token_api, data=data)
        access_token = token_response.json().get('access_token')

        id_token = token_response.json().get('id_token')
        print("token_response", token_response)
        print("access_token: ", access_token)

        # 카카오 계정 정보 가져오기
        user_info = requests.get('https://kapi.kakao.com/v2/user/me',
                                 headers={"Authorization": f"Bearer {access_token}"})
        user_info_json = user_info.json()
        print(user_info_json)
        kakao_id = user_info_json['id']
        nickname = user_info_json['properties']['nickname']
        email = user_info_json['kakao_account'].get('email', None)
        print("email", email)
        if email is None:
            raise KakaoException()

        profile_image = user_info_json['properties'].get('profile_image', None)  # 프로필 이미지 URL 가져오기

        try:
            user_profile = UserProfile.objects.get(kakao_id=kakao_id)
            user = user_profile.user

            # 이미 가입된 유저라면
            if user_profile.user_type != 'kakao':
                raise KakaoException()
            token = AccessToken.for_user(user)

            # 기타 필요한 정보 추가
            token['username'] = user.username
            token['email'] = user.email

            refresh = RefreshToken.for_user(user)  # refresh_token 발급

            # 프로필 정보 업데이트
            user_profile.realname = nickname
            user_profile.profile_image = profile_image
            user_profile.save()

            response = HttpResponseRedirect(FRONT_URL)
            response.set_cookie('token', str(token))
            response.set_cookie('refresh_token', str(refresh))

            return response
            # return JsonResponse({
            #     "token": str(token),
            #     "refresh_token": str(refresh),
            # }, status=200)

        except UserProfile.DoesNotExist:
            # ...
            user = User.objects.create_user(email=email, username=nickname)  # 새로운 유저 생성
            user_profile = UserProfile.objects.create(user=user, user_type='kakao', realname=nickname,
                                                      profile_image=profile_image, kakao_id=kakao_id)  # 프로필 생성
            token = AccessToken.for_user(user)

            # 기타 필요한 정보 추가
            token['username'] = user.username
            token['email'] = user.email

            refresh = RefreshToken.for_user(user)  # refresh_token 발급
            
            response = HttpResponseRedirect(FRONT_URL)
            response.set_cookie('token', str(token))
            response.set_cookie('refresh_token', str(refresh))
            
            return response

            # return JsonResponse({
            #     "token": str(token),
            #     "refresh_token": str(refresh),
            # }, status=200)
        except KakaoException:
            return redirect("http://127.0.0.1:8000/api/")


class KakaoLogin(SocialLoginView):
    adapter_class = kakao_views.KakaoOAuth2Adapter
    client_class = OAuth2Client