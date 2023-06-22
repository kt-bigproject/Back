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
    path('blog/', include('blog.urls')),
    # 글씨 연습 이미지 업로드
    path('practice/', include('practice.urls')),
    path('temp/', include('temp.urls')),
    path('game/', include('game.urls')),
    path('font/', include('font_blog.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
