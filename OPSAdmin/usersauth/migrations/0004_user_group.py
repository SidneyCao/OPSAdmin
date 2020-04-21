# Generated by Django 3.0.5 on 2020-04-14 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersauth', '0003_remove_user_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='group',
            field=models.ManyToManyField(related_name='user_group_set', to='usersauth.UserGroup', verbose_name='用户组属'),
        ),
    ]
