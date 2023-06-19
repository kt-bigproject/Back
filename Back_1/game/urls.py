from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import PracticeContentView, SentenceContentView, SyllableContentView, WordContentView, PredictAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('sentence', SentenceContentView)
router.register('syllable', SyllableContentView)
router.register('word', WordContentView)
router.register('upload', PracticeContentView)

urlpatterns =[
    path('', include(router.urls)),
    path('predict/', PredictAPIView.as_view(), name='predict'),
]

# if 'practice' in settings.INSTALLED_APPS:
#     urlpatterns += static(settings.PRACTICE_MEDIA_ROOT, document_root=settings.PRACTICE_MEDIA_ROOT)