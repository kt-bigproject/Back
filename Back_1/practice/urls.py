from django.urls import path, include
from .views import PracticeContentView, SentenceContentView
from rest_framework.routers import DefaultRouter

router_s = DefaultRouter()
router_s.register('sentence', SentenceContentView)

router_u = DefaultRouter()
router_u.register('upload', PracticeContentView)

urlpatterns =[
    path('', include(router_u.urls)),
    path('', include(router_s.urls)), # 필요한지
]