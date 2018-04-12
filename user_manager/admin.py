# -*- coding:utf-8 -*-
from django.contrib import admin
from user_manager import models
from user_manager.auth_admin import UserProfileAdmin
from hosts import models as hosts_models
# Register your models here.


class HostAdmin(admin.ModelAdmin):
    # 页面中可更改
    # list_editable = ('ip_address',)
    list_display = ('hostname', 'ip_address', 'port', 'idc', 'system_type', 'enabled')
    search_fields = ('hostname', 'ip_address')
    list_filter = ('idc', 'system_type')


class HostUserAdmin(admin.ModelAdmin):
    list_display = ('auth_type', 'username', 'password')


class BindHostToUserAdmin(admin.ModelAdmin):
    list_display = ('host', 'get_host_user', 'get_application_type', 'get_business_group')
    filter_horizontal = ('application_type', 'business_group', 'host_user')


class IDCAdmin(admin.ModelAdmin):
    list_display = ('name',)


class BusinessGroupAdmin(admin.ModelAdmin):
    list_display = ('business', 'function', 'environments')


class ApplicationTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'product')


class TaskLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'task_type', 'user', 'get_hosts', 'cmd_text')


class TaskLogDetailAdmin(admin.ModelAdmin):
    list_display = ('child_of_task', 'bind_host', 'result')


admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(hosts_models.Host, HostAdmin)
admin.site.register(hosts_models.HostUser, HostUserAdmin)
admin.site.register(hosts_models.IDC, IDCAdmin)
admin.site.register(hosts_models.BusinessGroup, BusinessGroupAdmin)
admin.site.register(hosts_models.ApplicationType, ApplicationTypeAdmin)
admin.site.register(hosts_models.BindHostToUser, BindHostToUserAdmin)
admin.site.register(hosts_models.TaskLog, TaskLogAdmin)
admin.site.register(hosts_models.TaskLogDetail, TaskLogDetailAdmin)
