from django.db import models


class Host(models.Model):
    hostname = models.CharField(max_length=64)
    ip_address = models.GenericIPAddressField(unique=True)
    port = models.IntegerField(default=22)
    idc = models.ForeignKey('IDC', on_delete=models.CASCADE)
    system_type_choices = (
        ('linux', 'Linux'),
        ('windows', 'Windows'),
    )
    system_type = models.CharField(choices=system_type_choices, max_length=32, default='linux')
    enabled = models.BooleanField(default=True)
    memo = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s(%s)" % (self.hostname, self.ip_address)

    class Meta:
        app_label = "user_manager"
        verbose_name = u'主机列表'
        verbose_name_plural = u"主机列表"


class IDC(models.Model):
    name = models.CharField(unique=True, max_length=64)
    memo = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = "user_manager"


class HostUser(models.Model):
    auth_type_choices = (
        ('ssh-password', 'SSH/PASSWORD'),
        ('ssh-key', 'SSH/KEY'),
        # 增加windows登录方法
    )
    auth_type = models.CharField(choices=auth_type_choices, max_length=32, default='ssh-password')
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=128, blank=True, null=True)
    memo = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return "(%s)%s" % (self.auth_type, self.username)

    class Meta:
        app_label = "user_manager"
        unique_together = ('auth_type', 'username', 'password')
        verbose_name = u'远程主机用户'
        verbose_name_plural = u"远程主机用户"


class BusinessGroup(models.Model):
    name = models.CharField(unique=True, max_length=64)
    memo = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = "user_manager"
        verbose_name = u'项目'
        verbose_name_plural = u"项目"


class ApplicationType(models.Model):
    name = models.CharField(unique=True, max_length=64)
    memo = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = "user_manager"
        verbose_name = u'应用类型'
        verbose_name_plural = u"应用类型"


class BindHostToUser(models.Model):
    host = models.ForeignKey("Host", on_delete=models.CASCADE)
    host_user = models.ManyToManyField("HostUser")
    application_type = models.ManyToManyField("ApplicationType")
    business_group = models.ManyToManyField("BusinessGroup")

    class Meta:
        app_label = "user_manager"
        verbose_name = u'主机所属项目和应用类型'
        verbose_name_plural = u"主机所属项目和应用类型"

    def __unicode__(self):
        return '%s' % self.host.hostname

    def get_application_type(self):

        return ','.join([g.name for g in self.application_type.select_related()])

    def get_business_group(self):

        return ','.join([g.name for g in self.business_group.select_related()])
