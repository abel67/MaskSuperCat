# Generated by Django 2.1.7 on 2019-04-10 09:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0026_auto_20190409_0822'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 10, 9, 47, 1, 941290), verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, null=True, verbose_name='邮箱'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=11, null=True, verbose_name='手机'),
        ),
    ]
