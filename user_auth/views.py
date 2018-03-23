import warnings
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,)
from django.urls import reverse, reverse_lazy
from django.shortcuts import resolve_url
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,)
from django.template.response import TemplateResponse
# Create your views here.


class RemovedInDjango21Warning(DeprecationWarning):
    pass


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


@login_required
def password_change(request,
                    template_name='accounts/password_change_form.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    extra_context=None):
    warnings.warn("The password_change() view is superseded by the "
                  "class-based PasswordChangeView().",
                  RemovedInDjango21Warning, stacklevel=2)
    if post_change_redirect is None:
        post_change_redirect = reverse('password_change_done')
    else:
        post_change_redirect = resolve_url(post_change_redirect)
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Updating the password logs out all other sessions for the user
            # except the current one.
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
        'title': 'Password change',
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


@login_required
def password_change_done(request,
                         template_name='registration/password_change_done.html',
                         extra_context=None):
    warnings.warn("The password_change_done() view is superseded by the "
                  "class-based PasswordChangeDoneView().",
                  RemovedInDjango21Warning, stacklevel=2)
    context = {
        'title': 'Password change successful',
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)
