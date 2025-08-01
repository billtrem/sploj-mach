from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
]

# Serve media files in both DEBUG and production (good for small projects)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
