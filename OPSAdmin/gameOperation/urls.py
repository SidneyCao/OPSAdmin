from django.urls import path, include
from . import views

app_name = 'gameOperation'

urlpatterns = [
    path('change-notice', views.changeNotice, name='changeNotice'),
    path('change-notice/exec', views.changeNoticeExec, name='changeNoticeExec'),
    path('change-time', views.changeTime, name='changeTime'),
    path('change-time/exec', views.changeTimeExec, name='changeTimeExec'),
    path('change-time/exec/stop', views.changeTimeExecStop, name='changeTimeExecStop'),
    path('change-time/exec/delete', views.changeTimeExecDelete, name='changeTimeExecDelete'),
    path('change-time/exec/restore', views.changeTimeExecRestore, name='changeTimeExecRestore'),
    path('change-time/exec/start', views.changeTimeExecStart, name='changeTimeExecStart'),
]