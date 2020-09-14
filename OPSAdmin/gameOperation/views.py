from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
import os, time, datetime
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from opsdash.views import writeOperationLog
# Create your views here.

monitorFile = '/home/langrisser-list/conf/qa_notice.txt'
IsoTimeFormat='%Y-%m-%d %H:%M:%S'
operationLogFile = settings.OPER_LOG_FILE

@login_required
def changeNotice(request):
    with open(monitorFile, 'r+') as fileRead:
        currentContent = fileRead.read() 
    lastChangeTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(monitorFile)))
    return render(request, 'gameOperation/changeNotice.html',context={'lastChangeTime': lastChangeTime,
                                                                      'currentContent': currentContent                
                                                                    })

@login_required
@csrf_exempt
def changeNoticeExec(request):

    currentUser = request.user

    if request.is_ajax:
        fileObj = request.FILES.get('file')
        #上传文件
        if fileObj:
            dir = '/home/langrisser-list/conf/'
            if not os.path.isdir(dir):
                os.mkdir(dir)
            uploadFile = "%s/%s" % (dir, fileObj.name)
            with open(uploadFile, 'wb') as newFile:
                for chunk in fileObj.chunks():
                    newFile.write(chunk)
            operLogMessage = datetime.datetime.now().strftime(IsoTimeFormat)+' '+currentUser.username+' 上传公告文件%s成功。' %fileObj.name
            writeOperationLog(operLogMessage)
            #获取新文件时间
            lastChangeTime = time.strftime(IsoTimeFormat, time.localtime(os.path.getmtime(monitorFile)))
            #获取新文件内容
            with open(monitorFile, 'r+') as fileRead:
                currentContent = fileRead.read() 
        return JsonResponse({'fileName':'%s' %fileObj.name, 'lastChangeTime':'%s' %lastChangeTime, 'currentContent':"%s" %currentContent})
    else:
        raise Http403

@login_required
def changeTime(request):
    qaCurrentTime = os.popen('/home/caojiawei/shell/get_qa_time.sh 2>&1').read()
    reviewCurrentTime=os.popen('/home/caojiawei/shell/get_review_time.sh 2>&1').read()
    oftCurrentTime=os.popen('/home/caojiawei/shell/get_oft_time.sh 2>&1').read()
    with open('/home/caojiawei/shell/qa_change_time.log','r+') as qaRead:
        qaOperLog = ("".join(qaRead.readlines()[0:60]))
    with open('/home/caojiawei/shell/review_change_time.log','r+') as reviewRead:
        reviewOperLog = ("".join(reviewRead.readlines()[0:60]))
    with open('/home/caojiawei/shell/oft_change_time.log','r+') as oftRead:
        oftOperLog = ("".join(oftRead.readlines()[0:60]))  
    return render(request, 'gameOperation/changeTime.html',context={'qaCurrentTime': qaCurrentTime,
                                                                    'reviewCurrentTime': reviewCurrentTime,  
                                                                    'oftCurrentTime': oftCurrentTime,
                                                                    'qaOperLog': qaOperLog,
                                                                    'reviewOperLog': reviewOperLog,
                                                                    'oftOperLog': oftOperLog
                                                                    })

@login_required
@csrf_exempt
def changeTimeExec(request):
    if request.is_ajax:
        execType = request.POST.get('execType')
        date = request.POST.get('date')
        response = os.popen('/home/caojiawei/shell/change_%s_time.sh %s 2>&1' %(execType, date)).read()
        if('invalid' in response or 'Invalid' in response):
            log=datetime.datetime.now().strftime(IsoTimeFormat)+' Error!'+'\n'+'服务器时间修改失败 '+response
        else:
            log=datetime.datetime.now().strftime(IsoTimeFormat)+' Successful!'+'\n'+'服务器时间成功修改为 '+response
        with open('/home/caojiawei/shell/%s_change_time.log' %execType,'r+') as fRead:
            conRead = fRead.read()
            fRead.seek(0,0)
            fRead.write(log+'\n'+'\n'+conRead)
        with open('/home/caojiawei/shell/%s_change_time.log' %execType,'r+') as fRead:
            currentLog = ("".join(fRead.readlines()[0:60]))
        currentTime = os.popen('/home/caojiawei/shell/get_%s_time.sh 2>&1' %execType).read()
        return JsonResponse({'currentTime':currentTime, 'currentLog':currentLog})
    else:
        raise Http403


@login_required
@csrf_exempt
def changeTimeExecStop(request):
    if request.is_ajax:
        execType = request.POST.get('execType')
        process = request.POST.get('process')
        if(process == 'stop'):
            os.popen('/home/langrisser-shell-scripts/Server/%s/ts_stopserver.sh 2>&1 > /dev/null' %execType)
            time.sleep(120)
            res = os.popen('/home/langrisser-shell-scripts/Server/%s/check_process.sh' %execType).read()
            if('Process Stop Success' in res):
                return JsonResponse({"process":"stop", "status":"success"})
            else:
                return JsonResponse({"process":"stop", "status":"fail"})
    else:
        raise Http403

@login_required
@csrf_exempt
def changeTimeExecDelete(request):
    if request.is_ajax:
        execType = request.POST.get('execType')
        process = request.POST.get('process')
        if(process == 'delete'):
            os.popen('/home/langrisser-shell-scripts/Server/%s/delete_logs.sh 2>&1' %execType)
            return JsonResponse({"process":"delete", "status":"success"})
    else:
        raise Http403

@login_required
@csrf_exempt
def changeTimeExecRestore(request):
    if request.is_ajax:
        execType = request.POST.get('execType')
        process = request.POST.get('process')
        if(process == 'restore'):
            date = os.popen("date '+%Y-%m-%d %H:%M:%S'").read()
            response = os.popen('/home/caojiawei/shell/change_%s_time.sh %s 2>&1' %(execType, date)).read()
            if('invalid' in response or 'Invalid' in response):
                log=datetime.datetime.now().strftime(IsoTimeFormat)+' Error!'+'\n'+'服务器时间恢复失败 '+response
            else:
                log=datetime.datetime.now().strftime(IsoTimeFormat)+' Successful!'+'\n'+'服务器时间成功恢复为 '+response
            with open('/home/caojiawei/shell/%s_change_time.log' %execType,'r+') as fRead:
                conRead = fRead.read()
                fRead.seek(0,0)
                fRead.write(log+'\n'+'\n'+conRead)
            with open('/home/caojiawei/shell/%s_change_time.log' %execType,'r+') as fRead:
                currentLog = ("".join(fRead.readlines()[0:60]))
            currentTime = os.popen('/home/caojiawei/shell/get_%s_time.sh 2>&1' %execType).read()
            return JsonResponse({'currentTime':currentTime, 'currentLog':currentLog, "process":"restore", "status":"success"})
    else:
        raise Http403

@login_required
@csrf_exempt
def changeTimeExecStart(request):
    if request.is_ajax:
        execType = request.POST.get('execType')
        process = request.POST.get('process')
        if(process == 'start'):
            os.popen('/home/langrisser-shell-scripts/Server/%s/ts_startserver.sh 2>&1 > /dev/null' %execType)
        return JsonResponse({"process":"start", "status":"success"})
    else:
        raise Http403