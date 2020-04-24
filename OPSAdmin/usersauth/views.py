from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .form import *


# Create your views here.


@login_required
def index(request):
    return render(request, 'usersauth/index.html', {'title': 'first index'})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        #requst.POST.get 获取的是 <input name="username">
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('usersauth:index')) 
            else:
                return HttpResponse("You account was inactive")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'usersauth/login.html', {})