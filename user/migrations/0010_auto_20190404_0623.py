# Generated by Django 2.1.7 on 2019-04-04 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20190404_0401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='type',
            field=models.SmallIntegerField(choices=[(1, '菜单'), (2, '功能')], verbose_name='类型'),
        ),
    ]