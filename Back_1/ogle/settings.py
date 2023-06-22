from pathlib import Path
from datetime import timedelta
from . import my_settings
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-0w7!0&+_=z8n*^v$im@pk-%mp0nj!+(56(v1b2g(8xm-ic0uzj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

#AUTH_USER_MODEL = 'sign.User' 


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    "corsheaders",

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.kakao',
    'allauth.socialaccount.providers.naver',
    'allauth.socialaccount.providers.google',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'dj_rest_auth',
    'dj_rest_auth.registration',

    'api',
    'blog',
    'practice',
    'temp',
    'game',
    'font_blog',
    
    'django_filters',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
PRACTICE_MEDIA_ROOT = os.path.join(BASE_DIR, 'practice', 'media')
GAME_MEDIA_ROOT = os.path.join(BASE_DIR, 'game', 'media')

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",	
    # corshaers는 최상단에
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

# CORS_ALLOWED_ORIGINS = True

# CORS_ORIGIN_WHITELIST = [
#     "http://localhost:3000",
#     "http://localhost:8000",
#     "http://127.0.0.1:8000",
# ]

ROOT_URLCONF = 'ogle.urls'
SITE_ID=1

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ogle.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/


LANGUAGE_CODE = "ko"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# my_setting.py
DATABASES = my_settings.DATABASES

SECRET_KEY = my_settings.SECRET_KEY

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES':[
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
    	'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticated', # 인증된 사용자만 접근
        # 'rest_framework.permissions.IsAdminUser', # 관리자만 접근
        'rest_framework.permissions.AllowAny', # 누구나 접근
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],

}

REST_USE_JWT = True

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5), # ACCESS Token의 유효기간
    'REFRESH_TOKEN_LIFETIME': timedelta(days=50), # Refresh 토큰의 유효기간 
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',

    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# 회원가입시 필수 이메일을 필수항목으로 만들기
ACCOUNT_EMAIL_REQUIRED = True  
# 이메일 인증 받기
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# 이메일 인증 링크 클릭시 홈페이지로 이동
ACCOUNT_CONFIRM_EMAIL_ON_GET = True

# 로그인 성공후 이동하는 URL
LOGIN_REDIRECT_URL = '/api/logout'

# 로그아웃시 이동하는 URL
LOGOUT_REDIRECT_URL = '/api/login' 

# gmail의 gmail email
EMAIL_HOST_USER = 'ogleogle1039@gmail.com'

# 구글 앱 비밀번호
EMAIL_HOST_PASSWORD = 'xfhlogxivhcxanxt'

# 보내지는 EMAIL 앞에 붙는 이름
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[이메일 인증] '

# EMAIL 유효 기간
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1

# 사용할 도메인 주소
EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT= 587

EMAIL_USE_TLS  = True

SESSION_COOKIE_PATH = "/"

# 네이버 API 키
NAVER_CLIENT_ID = my_settings.NAVER_CLIENT_ID
NAVER_CLIENT_SECRET = my_settings.NAVER_CLIENT_SECRET

SOCIAL_AUTH_GOOGLE_CLIENT_ID = my_settings.SOCIAL_AUTH_GOOGLE_CLIENT_ID
SOCIAL_AUTH_GOOGLE_SECRET = my_settings.SOCIAL_AUTH_GOOGLE_SECRET
STATE = my_settings.STATE

