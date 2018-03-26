# -*- coding:utf-8 -*-
from django.contrib import admin
from user_manager import models
from user_manager.auth_admin import UserProfileAdmin
from hosts import models as hosts_models
# Register your models here.
admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(hosts_models.Host)
admin.site.register(hosts_models.HostUser)
admin.site.register(hosts_models.BusinessGroup)
admin.site.register(hosts_models.ApplicationType)
admin.site.register(hosts_models.BindHostToUser)