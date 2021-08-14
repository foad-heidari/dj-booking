
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from main_app import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("booking/", include("booking.urls"))
]

# Debug mode
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
