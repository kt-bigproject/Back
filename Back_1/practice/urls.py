from django.urls import path, include
from .views import PracticeContentView, SentenceContentView, PredictAPIView
from rest_framework.routers import DefaultRouter

router_s = DefaultRouter()
router_s.register('sentence', SentenceContentView)

router_u = DefaultRouter()
router_u.register('upload', PracticeContentView)

router_predict = DefaultRouter()
router_predict.register('predict', PredictAPIView, basename='predict')

urlpatterns =[
    path('', include(router_u.urls)),
    path('', include(router_s.urls)), # 문장 업로드(어드민 페이지에도 있음)
    path('', include(router_predict.urls)),
]