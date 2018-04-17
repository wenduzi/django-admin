from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def week_report(request):
    return render(request, 'reports/week_report.html')


@login_required
def month_report(request):
    return render(request, 'reports/month_report.html')