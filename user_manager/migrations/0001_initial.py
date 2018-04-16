# Generated by Django 2.0.3 on 2018-04-13 07:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=64, unique=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=32, verbose_name='名字')),
                ('token', models.CharField(blank=True, default=None, max_length=128, null=True, verbose_name='token')),
                ('department', models.CharField(blank=True, default=None, max_length=32, null=True, verbose_name='部门')),
                ('mobile', models.CharField(blank=True, default=None, max_length=32, null=True, verbose_name='手机')),
                ('memo', models.TextField(blank=True, default=None, null=True, verbose_name='备注')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '00-用户信息',
                'verbose_name_plural': '00-用户信息',
            },
        ),
        migrations.CreateModel(
            name='ApplicationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('APP', 'APP'), ('DB', 'DB'), ('APP+DB', 'APP+DB')], default='app', max_length=64)),
                ('product', models.CharField(max_length=64, null=True)),
                ('memo', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': '05-应用类型',
                'verbose_name_plural': '05-应用类型',
            },
        ),
        migrations.CreateModel(
            name='BindHostToUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('application_type', models.ManyToManyField(to='user_manager.ApplicationType')),
            ],
            options={
                'verbose_name': '06-主机-项目-应用绑定',
                'verbose_name_plural': '06-主机-项目-应用绑定',
            },
        ),
        migrations.CreateModel(
            name='BusinessGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business', models.CharField(blank=True, max_length=64, null=True)),
                ('function', models.CharField(blank=True, max_length=64, null=True)),
                ('environments', models.CharField(choices=[('生产', '生产'), ('容灾', '容灾'), ('开发', '开发'), ('测试', '测试')], default='app', max_length=64)),
                ('memo', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': '04-项目分类',
                'verbose_name_plural': '04-项目分类',
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=64)),
                ('ip_address', models.GenericIPAddressField(unique=True)),
                ('port', models.IntegerField(default=22)),
                ('system_type', models.CharField(choices=[('linux', 'Linux'), ('windows', 'Windows')], default='linux', max_length=32)),
                ('enabled', models.BooleanField(default=True)),
                ('memo', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '01-主机',
                'verbose_name_plural': '01-主机',
            },
        ),
        migrations.CreateModel(
            name='HostUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auth_type', models.CharField(choices=[('ssh-password', 'SSH/PASSWORD'), ('ssh-key', 'SSH/KEY'), ('ntlm', 'NTLM'), ('kerberos', 'KERBEROS')], default='ssh-password', max_length=32)),
                ('label_name', models.CharField(blank=True, max_length=64, null=True)),
                ('username', models.CharField(max_length=64)),
                ('password', models.CharField(blank=True, max_length=128, null=True)),
                ('memo', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': '02-主机账户密码',
                'verbose_name_plural': '02-主机账户密码',
            },
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('memo', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': '03-数据中心',
                'verbose_name_plural': '03-数据中心',
            },
        ),
        migrations.CreateModel(
            name='TaskLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('task_type', models.CharField(choices=[('multi_cmd', '命令'), ('cron_job', '定时任务')], max_length=50)),
                ('cmd_text', models.TextField()),
                ('expire_time', models.IntegerField(default=30)),
                ('task_pid', models.IntegerField(default=0)),
                ('note', models.CharField(blank=True, max_length=100, null=True)),
                ('hosts', models.ManyToManyField(to='user_manager.BindHostToUser')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'CMD任务',
                'verbose_name_plural': 'CMD任务',
            },
        ),
        migrations.CreateModel(
            name='TaskLogDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('end_time', models.DateTimeField(auto_now_add=True)),
                ('event_log', models.TextField()),
                ('result', models.CharField(choices=[('success', 'Success'), ('failed', 'Failed'), ('unknown', 'Unknown')], default='unknown', max_length=30)),
                ('note', models.CharField(blank=True, max_length=100)),
                ('bind_host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_manager.BindHostToUser')),
                ('child_of_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_manager.TaskLog')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'CMD子任务日志',
                'verbose_name_plural': 'CMD子任务日志',
            },
        ),
        migrations.CreateModel(
            name='TaskSummary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('cmd_text', models.TextField()),
                ('task_result', models.CharField(default='unknown', max_length=30)),
                ('task_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_manager.TaskLog')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'CMD任务汇总',
                'verbose_name_plural': 'CMD任务汇总',
            },
        ),
        migrations.AlterUniqueTogether(
            name='hostuser',
            unique_together={('auth_type', 'username', 'password')},
        ),
        migrations.AddField(
            model_name='host',
            name='idc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_manager.IDC'),
        ),
        migrations.AlterUniqueTogether(
            name='businessgroup',
            unique_together={('business', 'function', 'environments')},
        ),
        migrations.AddField(
            model_name='bindhosttouser',
            name='business_group',
            field=models.ManyToManyField(to='user_manager.BusinessGroup'),
        ),
        migrations.AddField(
            model_name='bindhosttouser',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_manager.Host'),
        ),
        migrations.AddField(
            model_name='bindhosttouser',
            name='host_user',
            field=models.ManyToManyField(to='user_manager.HostUser'),
        ),
        migrations.AlterUniqueTogether(
            name='applicationtype',
            unique_together={('name', 'product')},
        ),
        migrations.AddField(
            model_name='userprofile',
            name='application_type',
            field=models.ManyToManyField(blank=True, to='user_manager.ApplicationType'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='bind_hosts',
            field=models.ManyToManyField(blank=True, to='user_manager.BindHostToUser'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='business_group',
            field=models.ManyToManyField(blank=True, to='user_manager.BusinessGroup'),
        ),
    ]
