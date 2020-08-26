from django.urls import path, include
from . import views

app_name = 'systemAdmin'

urlpatterns = [
    path('change_notice', views.changeNotice, name='changeNotice'),
]