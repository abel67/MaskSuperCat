# Generated by Django 2.1.7 on 2019-04-10 09:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0030_remove_user_create_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 10, 9, 50, 38, 941139), verbose_name='创建时间'),
        ),
    ]
