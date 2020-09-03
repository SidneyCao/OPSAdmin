from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
import os, time, datetime
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@login_required
def changeNotice(request):
    return render(request, 'gameOperation/changeNotice.html')

@login_required
@csrf_exempt
def changeNoticeExec(request):
    if request.is_ajax:
        fileObj = request.FILES.get('file')
        if fileObj:
            dir = '/home/langrisser-list/conf/'
            if not os.path.isdir(dir):
                os.mkdir(dir)
            uploadFile = "%s/%s" % (dir, fileObj.name)
            with open(uploadFile, 'wb') as newFile:
                for chunk in fileObj.chunks():
                    newFile.write(chunk)
            
        return JsonResponse({'fileName':'%s' %fileObj.name})
    else:
        raise Http403