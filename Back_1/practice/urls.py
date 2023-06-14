from django.urls import path, include
from .views import PracticeContentView
from rest_framework.routers import DefaultRouter

# router_p = DefaultRouter()
# router_p.register('PracticeContent', PracticeContentView)

router_u = DefaultRouter()
router_u.register('upload', PracticeContentView)

urlpatterns =[
    path('', include(router_u.urls))
]