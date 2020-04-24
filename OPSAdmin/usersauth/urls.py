from django.urls import path, include

from . import views

app_name = 'usersauth'

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login/', views.user_login, name='user_login'),
]