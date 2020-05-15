from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
    return render(request, 'opsdash/dashboard.html',{})

@login_required
def upload_notice(request):
    return render(request, 'opsdash/upload_notice.html',{})