from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from .media_views import serve_media

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('doctors.urls')),
    path('', include('patients.urls')),
]

# Serve media files in both development and production
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve_media, name='media'),
]

# Serve static files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Additional media file serving for production
if not settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
