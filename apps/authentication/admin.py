# apps/authentication/admin.py
from django.contrib import admin
from apps.authentication.models import UserProfile


admin.site.register(UserProfile)