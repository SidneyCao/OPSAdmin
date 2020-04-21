from django.contrib import admin
from .models import User, UserGroup
from django.contrib.auth.admin import UserAdmin, GroupAdmin
# Register your models here.

admin.site.register(User, UserAdmin)
