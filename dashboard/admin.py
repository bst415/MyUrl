from django.contrib import admin
from .models import user_urls, public_urls

# Register your models here.

admin.site.register(user_urls)
admin.site.register(public_urls)