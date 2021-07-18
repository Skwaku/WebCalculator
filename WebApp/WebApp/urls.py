from django.conf.urls import url
from django.urls import path, include
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static


urlpatterns =[
    url('admin/', admin.site.urls),
    path('', include('calculator.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

