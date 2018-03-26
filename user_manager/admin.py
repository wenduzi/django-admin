# -*- coding:utf-8 -*-
from django.contrib import admin
from user_manager import models
from user_manager.auth_admin import UserProfileAdmin
# Register your models here.
admin.site.register(models.UserProfile, UserProfileAdmin)
