#ogle/urls.py
from django.urls import path, include
from django.contrib import admin
from django.conf import settings	
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from game import views

router = DefaultRouter()
router.register('PracticeContent', views.PracticeContentView, 'PracticeContent')

urlpatterns = [
    path("admin/", admin.site.urls),
    # path('rest-auth/', include('sign.urls')),
    path('api/', include('api.urls')),
    path('api/blog/', include('blog.urls')),
    # 글씨 연습 이미지 업로드
    path('api/practice/', include('practice.urls')),
    path('api/temp/', include('temp.urls')),
    path('api/game/', include('game.urls')),
    path('api/font/', include('font_blog.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
