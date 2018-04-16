from django.shortcuts import (render, HttpResponse)
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from hosts import task, utils
import json


# 批量命令
@login_required()
def command(request):
    return render(request, 'hosts/command.html')


@login_required()
@csrf_exempt
def submit_cmd(request):
    task_obj = task.Task(request)
    res = task_obj.handle()
    return HttpResponse(json.dumps(res))


@login_required()
def get_cmd_result(request):
    task_obj = task.Task(request)
    res = task_obj.get_cmd_result()
    return HttpResponse(json.dumps(res, default=utils.json_date_handler))


# 定时任务
@login_required()
def job(request):
    return render(request, 'hosts/job.html')


# 审计
@login_required()
def audit(request):
    return render(request, 'hosts/audit.html')
