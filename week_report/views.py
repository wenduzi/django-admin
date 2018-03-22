from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def week_report(request):
    return render(request, 'week_report.html')


@login_required
def month_report(request):
    return render(request, 'month_report.html')