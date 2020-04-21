# Generated by Django 3.0.5 on 2020-04-14 09:31

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('usersauth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.Group')),
                ('group_name', models.CharField(max_length=100, unique=True, verbose_name='用户组')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='group',
            field=models.ManyToManyField(related_name='user_group_set', to='usersauth.UserGroup', verbose_name='用户组属'),
        ),
    ]
