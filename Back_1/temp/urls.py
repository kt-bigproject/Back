# temp/urls.py
from django.urls import path, include
from .views import TempViewSet
from rest_framework.routers import DefaultRouter
from rest_framework import urls

router = DefaultRouter()
router.register('temp', TempViewSet, basename='temp')

app_name = 'temp'

urlpatterns =[
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
