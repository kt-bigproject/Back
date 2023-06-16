from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PredictAPIView

router_predict = DefaultRouter()
router_predict.register('predict', PredictAPIView, basename='predict')

urlpatterns = [
    path('', include(router_predict.urls)),
]

