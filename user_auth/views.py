from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


def user_login(requeset):
    login_err = ''
    if requeset.method == 'POST':
        username = requeset.POST.get('email')
        password = requeset.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(requeset, user)
            return HttpResponseRedirect('/')
        else:
            login_err = "Wrong username or password!"
    return render(requeset, 'accounts/login.html', {'login_err': login_err})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")
