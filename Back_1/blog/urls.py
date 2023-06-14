from django.urls import path, include
from .views import BlogViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter
from rest_framework import urls

router = DefaultRouter()
router.register('blog', BlogViewSet, basename='blog') # (게시글)
router.register('comment', CommentViewSet, basename='comment') # (댓글)


urlpatterns =[
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]