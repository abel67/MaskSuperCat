# Generated by Django 2.1.7 on 2019-04-09 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0025_auto_20190409_0817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.SmallIntegerField(choices=[(0, '管理员'), (1, '普通用户')]),
        ),
    ]
