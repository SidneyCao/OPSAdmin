# Generated by Django 3.0.5 on 2020-04-14 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usersauth', '0002_auto_20200414_0931'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='group',
        ),
    ]
