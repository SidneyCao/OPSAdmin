from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.conf import settings
from opsdash.views import writeOperationLog
import datetime
# Create your views here.

IsoTimeFormat='%Y-%m-%d %H:%M:%S'


def user_login(request,authentication_form=AuthenticationForm):
    if request.method == 'GET':
        cache.set('next', request.GET.get('next', None))
    err_message = ''
    if request.method == 'POST':
        #requst.POST.get 获取的是 <input name="username">
        username = request.POST.get('username')
        password = request.POST.get('password')
        nextUrl = cache.get('next')
        user = authenticate(username=username, password=password)        
        if user:
            login(request, user)
            currentUser = request.user
            operLogMessage = datetime.datetime.now().strftime(IsoTimeFormat)+' '+currentUser.username+' 登陆 成功。'
            writeOperationLog(operLogMessage)
            if nextUrl:
                cache.delete('next')
                return HttpResponseRedirect(reverse(nextUrl))
        else:
            err_message = '<div class="alert alert-danger"><p class="mb-0"><strong>ERROR!</strong></p>username or password not match!</strong></div>'
            return render(request, 'usersauth/login.html',{'err_message': err_message})
    else:
        return render(request, 'usersauth/login.html', {'err_message': err_message})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('usersauth:user_login'))
