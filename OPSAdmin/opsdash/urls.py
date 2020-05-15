from django.urls import path, include
from . import views

app_name = 'opsdash'

urlpatterns = [
    path('', views.index, name='index'),
    path('ops/upload_notice', views.upload_notice, name='upload_notice')
]