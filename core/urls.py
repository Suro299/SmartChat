from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("users.urls")),
    path("sc/", include("main.urls")),
    path("us/", include("about_us.urls")),
    path("sponsor/", include("sponsor.urls")),
    path("settings/", include("settings.urls")),
    path("chat/", include("chat.urls")),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
