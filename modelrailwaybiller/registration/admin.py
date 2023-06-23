from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import RailUser

admin.site.register(RailUser, UserAdmin)