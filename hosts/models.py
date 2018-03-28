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

    def __str__(self):
        return "%s(%s)" % (self.hostname, self.ip_address)

    class Meta:
        app_label = "user_manager"
        verbose_name = u'01-主机'
        verbose_name_plural = u"01-主机"


class IDC(models.Model):
    name = models.CharField(unique=True, max_length=64)
    memo = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = "user_manager"
        verbose_name = u'03-数据中心'
        verbose_name_plural = u"03-数据中心"


class HostUser(models.Model):
    auth_type_choices = (
        ('ssh-password', 'SSH/PASSWORD'),
        ('ssh-key', 'SSH/KEY'),
        ('ntlm', 'NTLM'),
        ('kerberos', 'KERBEROS'),
    )
    auth_type = models.CharField(choices=auth_type_choices, max_length=32, default='ssh-password')
    label_name = models.CharField(max_length=64, blank=True, null=True)
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=128, blank=True, null=True)
    memo = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s(%s)" % (self.username, self.label_name)

    class Meta:
        app_label = "user_manager"
        unique_together = ('auth_type', 'username', 'password')
        verbose_name = u'02-主机账户密码'
        verbose_name_plural = u"02-主机账户密码"


class BusinessGroup(models.Model):
    environments_choices = (
        ('生产', '生产'),
        ('容灾', '容灾'),
        ('开发', '开发'),
        ('测试', '测试'),
    )
    business = models.CharField(max_length=64)
    function = models.CharField(max_length=64, blank=True, null=True)
    environments = models.CharField(choices=environments_choices, max_length=64, default='app')
    memo = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s--%s--%s" % (self.business, self.function, self.environments)

    class Meta:
        app_label = "user_manager"
        unique_together = ('business', 'function', 'environments')
        verbose_name = u'04-项目分类'
        verbose_name_plural = u"04-项目分类"


class ApplicationType(models.Model):
    application_type_choices = (
        ('APP', 'APP'),
        ('DB', 'DB'),
        ('APP+DB', 'APP+DB'),
    )
    name = models.CharField(choices=application_type_choices, max_length=64, default='app')
    product = models.CharField(max_length=64, null=True)
    memo = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s(%s)" % (self.name, self.product)

    class Meta:
        app_label = "user_manager"
        unique_together = ('name', 'product')
        verbose_name = u'05-应用类型'
        verbose_name_plural = u"05-应用类型"


class BindHostToUser(models.Model):
    host = models.ForeignKey("Host", on_delete=models.CASCADE)
    host_user = models.ManyToManyField("HostUser")
    application_type = models.ManyToManyField("ApplicationType")
    business_group = models.ManyToManyField("BusinessGroup")

    class Meta:
        app_label = "user_manager"
        verbose_name = u'06-主机-项目-应用绑定'
        verbose_name_plural = u"06-主机-项目-应用绑定"

    def __str__(self):
        return '%s(%s)' % (self.host.hostname, self.host.ip_address)

    def get_host_user(self):

        return ','.join([g.username for g in self.host_user.select_related()])

    def get_application_type(self):

        return ','.join([g.name for g in self.application_type.select_related()])

    def get_business_group(self):

        return ','.join([g.business for g in self.business_group.select_related()])
