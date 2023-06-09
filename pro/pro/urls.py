
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('coplate.urls')),
    path("email-confirmation-done/",
        TemplateView.as_view(template_name="coplate/email=confirmation-done.html"),
        name="account_email_confirmation_done"),

]
