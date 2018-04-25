from django.shortcuts import (render, HttpResponse)
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from hosts import task, utils, models
from elasticsearch import Elasticsearch
import json
from django.utils import timezone


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


@login_required()
def get_cpu_usage(request):
    selected_host = request.GET.getlist('selected_host[]')
    for host_id in selected_host:
        host_id = host_id
        host = models.BindHostToUser.objects.get(id=host_id)
        hostname = host.host.hostname
    es = Elasticsearch(['11.11.66.148:9200'])
    query = {'query': {'term': {'name': 'jack'}}}
    es_result = es.search(index='metricbeat-6.2.4-2018.04.25', body=query)
    for h in es_result['aggregations']['envent_id']['buckets']:
        print(h)
    return HttpResponse(json.dumps(h, default=utils.json_date_handler))


# 定时任务
@login_required()
def job(request):
    return render(request, 'hosts/job.html')


# 审计
@login_required()
def audit(request):
    return render(request, 'hosts/audit.html')
