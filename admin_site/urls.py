"""admin_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from week_report import views as week_report_views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url, include


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^accounts/',include('user_auth.urls')),
    re_path('^$', week_report_views.week_report, name='week_report'),
    path('month_report', week_report_views.month_report, name='month_report'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
