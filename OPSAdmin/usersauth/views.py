from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout


# Create your views here.


@login_required
def index(request):
    return render(request, 'usersauth/index.html', {'title': 'first index'})


def user_login(request, authentication_form=AuthenticationForm):
    err_message = ''
    if request.method == 'POST':
        #requst.POST.get 获取的是 <input name="username">
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)        
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('usersauth:index')) 
        else:
            err_message = '<div class="alert alert-danger"><strong>username or password error!</strong></div>'
            return render(request, 'usersauth/login.html',{'err_message': err_message})
    else:
        return render(request, 'usersauth/login.html', {'err_message': err_message})