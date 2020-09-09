from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
import os, time, datetime
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

monitorFile = '/home/langrisser-list/conf/qa_notice.txt'
IsoTimeFormat='%Y-%m-%d %H:%M:%S'

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
            log=datetime.datetime.now().strftime(IsoTimeFormat)+' Error!'+'\n'+response
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
            time.sleep(10)
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
            os.popen('/home/langrisser-shell-scripts/Server/%s/delete_logs.sh 2>&1 > /home/langrisser-shell-scripts/Server/oft/delete_logs.log' %execType)
            return JsonResponse({"process":"delete", "status":"success"})
    else:
        raise Http403

@login_required
@csrf_exempt
def changeTimeExecRestore(request):
    if request.is_ajax:
        execType = request.POST.get('execType')
        process = request.POST.get('process')
        print(execType)
        print(process)
        return JsonResponse({"1":"1"})
    else:
        raise Http403

@login_required
@csrf_exempt
def changeTimeExecStart(request):
    if request.is_ajax:
        execType = request.POST.get('execType')
        process = request.POST.get('process')
        print(execType)
        print(process)
        return JsonResponse({"1":"1"})
    else:
        raise Http403