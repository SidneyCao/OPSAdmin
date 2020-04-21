from django.db import models

## import AbstractUser can customize new field 
from django.contrib.auth.models import AbstractUser, Group, Permission
# Create your models here.

class UserGroup(Group):
    group_name = models.CharField(max_length=100, unique=True, verbose_name=u'用户组')
    comment = models.TextField(blank=True, null=True, verbose_name=u'备注')
    




class User(AbstractUser):
    group = models.ManyToManyField(UserGroup, related_name='user_group_set', verbose_name=u'用户组属')
    
    class Meta:
        verbose_name_plural = u'Users Admin'


