from django.contrib import admin
from user_auth import models, custom_auth
from user_auth.auth_admin import UserProfileAdmin
# Register your models here.
admin.site.register(models.UserProfile,)
