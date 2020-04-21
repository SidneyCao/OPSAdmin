from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .form import *


# Create your views here.


@login_required
def index(request):
    return render(request, 'usersauth/index.html', {'title': 'first index'})


def login(request, authentication_form=AuthenticationForm):
    verify_err = ''
    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():
            if form.get_user() and form.get_user().is_active:
                pass
    else:
        form = authentication_form(request)
    return render(request, 'usersauth/login.html', {'title': '用户登录'})