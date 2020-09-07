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
        qaOperLog = ("".join(qaRead.readlines()[0:50]))
    with open('/home/caojiawei/shell/review_change_time.log','r+') as reviewRead:
        reviewOperLog = ("".join(reviewRead.readlines()[0:50]))
    with open('/home/caojiawei/shell/oft_change_time.log','r+') as oftRead:
        oftOperLog = ("".join(oftRead.readlines()[0:50]))  
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
        print(response)
    return JsonResponse({"1":"1"})
    