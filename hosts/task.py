from hosts import models
from django.db import transaction
from admin_site import settings
import subprocess
import os


class Task(object):
    def __init__(self, request):
        self.request = request
        self.task_type = self.request.POST.get('task_type')

    def handle(self):
        if self.task_type:
            if hasattr(self, self.task_type):
                func = getattr(self, self.task_type)
                return func()
            else:
                return TypeError

    @transaction.atomic
    def multi_cmd(self):
        # print(self.request.POST.get('task_type'))
        # print(self.request.POST.get('cmd_text'))
        # print(selected_host)
        selected_host = self.request.POST.getlist('selected_host[]')
        task_obj = models.TaskLog(
            user=self.request.user,
            task_type=self.task_type,
            cmd_text=self.request.POST.get('cmd_text'),
        )
        task_obj.save()
        # manytomany 需要创建对象后在添加
        # 列表前面加个*号可以除掉括号
        task_obj.hosts.add(*selected_host)
        for host_id in selected_host:
            obj = models.TaskLogDetail(
                child_of_task_id=task_obj.id,
                bind_host_id=host_id,
                event_log="N/A",
            )
            obj.save()
        p = subprocess.Popen([
            'python',
            settings.SCRIPT_ROOT,
            '-task_id', str(task_obj.id),
            '-run_type', settings.RunType,
        ], preexec_fn=os.setsid)
        print('----->pid:', p.pid)

        return {'task_id': task_obj.id}

    def get_cmd_result(self):
        task_id = self.request.GET.get('task_id')
        if task_id:
            res_list = models.TaskLogDetail.objects.filter(child_of_task=task_id)
            return list(res_list.values('id',
                                        'bind_host__host__hostname',
                                        'bind_host__host__ip_address',
                                        'date',
                                        'event_log',
                                        'result'
                                        ))

    def cron_job(self):
        pass
