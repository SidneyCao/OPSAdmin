from django.urls import path, include
from . import views

app_name = 'gameOperation'

urlpatterns = [
    path('change-notice', views.changeNotice, name='changeNotice'),
    path('change-notice/exec', views.changeNoticeExec, name='changeNoticeExec'),
]