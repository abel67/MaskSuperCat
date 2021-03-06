# Generated by Django 2.1.7 on 2019-04-04 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_auto_20190404_1006'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='identifier',
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=18, unique=True, verbose_name='名字'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=18, unique=True, verbose_name='用户账号'),
        ),
    ]
