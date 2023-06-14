from pathlib import Path

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

    

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth.registration',
    'sign',
    'blog',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ogle.urls'
SITE_ID=1

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_39',
        'USER': 'root',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

SECRET_KEY = "django-insecure-+d@0e(gyc7+e8yl6=5*jab^6hcj=*bj^=ub!xcnw$$h3&n%r4o"



REST_USE_JWT = True
# 회원가입시 필수 이메일을 필수항목으로 만들기

ACCOUNT_EMAIL_REQUIRED = True  
# 이메일 인증 받기
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# 이메일 인증 링크 클릭시 홈페이지로 이동
ACCOUNT_CONFIRM_EMAIL_ON_GET = True

# 로그인 성공후 이동하는 URL
LOGIN_REDIRECT_URL = '/accounts/logout'

# 로그아웃시 이동하는 URL
LOGOUT_REDIRECT_URL = '/accounts/login' 

# gmail의 gmail email
EMAIL_HOST_USER = 'a01034613077@gmail.com'

# 구글 앱 비밀번호
EMAIL_HOST_PASSWORD = 'dxelesgrswyeglzi'

# 보내지는 EMAIL 앞에 붙는 이름
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[이메일 인증] '

# EMAIL 유효 기간
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1

# 사용할 도메인 주소
EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT= 587

EMAIL_USE_TLS  = True
