from django.shortcuts import render

# Create your views here.


def file(request):
    return render(request, 'hosts/file.html')


def command(request):
    return render(request, 'hosts/command.html')


def job(request):
    return render(request, 'hosts/job.html')


def audit(request):
    return render(request, 'hosts/audit.html')
