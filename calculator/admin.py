from django.contrib import admin

from .models import *

admin.site.site_header = "WebCal"

admin.site.register(History)