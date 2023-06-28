# my_setting.py
DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_39',
        'USER': 'root',
        'PASSWORD': 'aivle',
        # 'HOST': 'ls-47ab0e27fb770fb5ef6de013bb5d20ec68ebbbe0.cfbesmzpzzdq.ap-northeast-2.rds.amazonaws.com',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

SECRET_KEY = "django-insecure-+d@0e(gyc7+e8yl6=5*jab^6hcj=*bj^=ub!xcnw$$h3&n%r4o"

NAVER_CLIENT_ID = 'f0Pepzs047CEvyYNv2yH'
NAVER_CLIENT_SECRET = 'ACTDBDacfC'

SOCIAL_AUTH_GOOGLE_CLIENT_ID = "878753331442-vf1sel470reappq52vgmjhufiiehqv1s.apps.googleusercontent.com"
SOCIAL_AUTH_GOOGLE_SECRET = "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"
STATE = 'VSDCSDC'