from django.shortcuts import (render, HttpResponse)
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from hosts import task
# from django.template import RequestContext

# Create your views here.


@login_required()
def file(request):
    return render(request, 'hosts/file.html')


@login_required()
def command(request):
    return render(request, 'hosts/command.html')


@login_required()
def job(request):
    return render(request, 'hosts/job.html')


@login_required()
def audit(request):
    return render(request, 'hosts/audit.html')


@login_required()
@csrf_exempt
def submit_cmd(request):
    print(request.POST)
    print(request.POST.get('task_type'))
    print(request.POST.get('cmd_text'))
    print(request.POST.getlist('selected_host[]'))
    task_obj=task.Task(request)
    task_obj.handle()
    return HttpResponse('DDD')
