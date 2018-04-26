from django.shortcuts import (render, HttpResponse)
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from hosts import task, utils, models
from elasticsearch import Elasticsearch
import json
import pytz
from pytz import timezone
from datetime import datetime, timedelta


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
    global host
    selected_host = request.GET.getlist('selected_host[]')
    for host_id in selected_host:
        host_id = host_id
        host = models.BindHostToUser.objects.get(id=host_id)
    es = Elasticsearch(['11.11.66.148:9200'], timeout=120)
    end_t = timezone('utc').localize(datetime.now()).astimezone(pytz.timezone('Asia/Shanghai'))
    start_t = end_t - timedelta(minutes=10)
    query = {"size": 10000, "query": {"bool": {"filter": [{"match": {"beat.hostname": host.host.hostname}},
                                           {"exists": {"field": "system.process.cpu.total.pct"}},
                                           {"range": {"@timestamp": {"gte": start_t, "lte": end_t}}}]
                                }}
             }
    es_result = es.search(index='metricbeat-6.2.4-2018.04.26', body=query)
    if es_result['hits']['total'] != 0:
        data_list = []
        for h in es_result['hits']['hits']:
            data = []
            timestamp = h['_source']['@timestamp']
            cpu_pct = h['_source']['system']['process']['cpu']['total']['pct']
            data.append(timestamp)
            data.append(cpu_pct)
            data_list.append(data)
            print(data)
        print(data_list)

    return HttpResponse(json.dumps(data_list, default=utils.json_date_handler))


# 定时任务
@login_required()
def job(request):
    return render(request, 'hosts/job.html')


# 审计
@login_required()
def audit(request):
    return render(request, 'hosts/audit.html')
