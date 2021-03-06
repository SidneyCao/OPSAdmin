from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
import datetime

operationLogFile = settings.OPER_LOG_FILE
IsoTimeFormat='%Y-%m-%d %H:%M:%S'

# Create your views here.
#记录操作日志
def writeOperationLog(operLogMessage):
    with open(operationLogFile,'r+') as fRead:
            conRead = fRead.read()
            fRead.seek(0,0)
            fRead.write(operLogMessage+'\n'+'\n'+conRead)

@login_required
def index(request):
    with open(operationLogFile, 'r+') as fRead:
        currentOperationLog = ("".join(fRead.readlines()[0:60]))
    return render(request, 'opsdash/operationLog.html', context={'currentOperationLog':currentOperationLog})

