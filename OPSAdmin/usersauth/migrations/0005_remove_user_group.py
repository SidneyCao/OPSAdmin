# Generated by Django 3.0.5 on 2020-04-14 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usersauth', '0004_user_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='group',
        ),
    ]