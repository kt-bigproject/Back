from django.urls import path, include
from .views import PracticeContentView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('upload', PracticeContentView)

urlpatterns =[
    path('', include(router.urls))
]