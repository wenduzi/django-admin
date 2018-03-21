from django.contrib import admin
from user_auth import models, custom_auth
# Register your models here.
admin.site.register(models.UserProfile)
