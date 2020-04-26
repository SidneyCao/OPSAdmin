from django.urls import path, include
from . import views

app_name = 'opsdash'

urlpatterns = [
    path('', views.index, name='index'),
]