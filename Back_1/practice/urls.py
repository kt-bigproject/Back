from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import PracticeContentView, SentenceContentView, PredictAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('sentence', SentenceContentView)
router.register('upload', PracticeContentView)
router.register('predict', PredictAPIView, basename='predict')

urlpatterns =[
    path('', include(router.urls)),
]

if 'practice' in settings.INSTALLED_APPS:
    urlpatterns += static(settings.PRACTICE_MEDIA_ROOT, document_root=settings.PRACTICE_MEDIA_ROOT)