from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
    currentUser = request.user 
    print(currentUser.username)
    OperationlogFile = '/home/caojiawei/shell/operationLog.log'
    with open(OperationlogFile, 'r+') as fRead:
        currentOperationLog = ("".join(fRead.readlines()[0:60]))
    return render(request, 'opsdash/operationLog.html', context={'currentOperationLog':currentOperationLog})

