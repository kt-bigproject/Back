from django.urls import path, include
from django.contrib import admin
from django.conf import settings	
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from practice import views

router = DefaultRouter()
router.register('PracticeContent', views.PracticeContentView, 'PracticeContent')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('rest-auth/', include('sign.urls')),
    path('blog/', include('blog.urls')),
    # 글씨 연습 이미지 업로드
    path('practice/', include('practice.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
