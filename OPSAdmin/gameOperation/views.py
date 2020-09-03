from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
import os, time, datetime
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@login_required
def changeNotice(request):
    monitorFile = '/home/langrisser-list/conf/0204qa_notice.txt'
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
            lastChangeTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime("%s/%s" % (dir, fileObj.name))))
            #获取新文件内容
            with open(uploadFile, 'r+') as fileRead:
                currentContent = fileRead.read() 
        return JsonResponse({'fileName':'%s' %fileObj.name, 'lastChangeTime':'%s' %lastChangeTime, 'currentContent':"%s" %currentContent})
    else:
        raise Http403