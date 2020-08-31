from django.urls import path, include
from . import views

app_name = 'systemAdmin'

urlpatterns = [
    path('upload-patch', views.uploadPatch, name='uploadPatch'),
]