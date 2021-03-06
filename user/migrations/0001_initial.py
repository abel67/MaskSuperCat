# Generated by Django 2.1.7 on 2019-03-15 10:37

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'msk_user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Interface',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=18, unique=True, verbose_name='接口名')),
                ('path', models.CharField(max_length=128, verbose_name='接口路径')),
                ('method', models.CharField(max_length=8, verbose_name='调用方法')),
                ('description', models.CharField(max_length=128, null=True, verbose_name='接口描述')),
            ],
            options={
                'db_table': 'msk_interface',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('menu_id', models.CharField(max_length=128, unique=True, verbose_name='菜单ID')),
                ('parent_id', models.CharField(max_length=128, verbose_name='父菜单ID')),
                ('path', models.CharField(max_length=128, verbose_name='菜单路径')),
                ('title', models.CharField(max_length=128, verbose_name='菜单标题')),
                ('icon', models.CharField(max_length=128, null=True, verbose_name='菜单图标')),
                ('permission', models.CharField(max_length=128, null=True, verbose_name='菜单权限标识')),
                ('type', models.CharField(choices=[(0, '菜单'), (1, '功能')], max_length=2, verbose_name='类型')),
                ('sort', models.IntegerField(verbose_name='排序')),
                ('is_lock', models.BooleanField(default=False, verbose_name='锁定')),
                ('api', models.ManyToManyField(db_table='menu_to_interface', to='user.Interface')),
            ],
            options={
                'db_table': 'msk_menu',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=18, unique=True, verbose_name='角色名')),
                ('code', models.CharField(max_length=128, null=True, verbose_name='角色代码')),
                ('description', models.CharField(max_length=128, null=True, verbose_name='角色描述')),
                ('permission', models.ManyToManyField(db_table='role_to_menu', to='user.Menu', verbose_name='角色权限')),
            ],
            options={
                'db_table': 'msk_role',
            },
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('route_id', models.CharField(max_length=128, unique=True, verbose_name='路由ID')),
                ('parent_id', models.CharField(max_length=128, verbose_name='父路由ID')),
                ('path', models.CharField(max_length=128, verbose_name='路由路径')),
                ('name', models.CharField(max_length=18, unique=True, verbose_name='路由名')),
                ('title', models.CharField(max_length=128, verbose_name='路由标题')),
                ('permission', models.CharField(max_length=128, verbose_name='路由权限标识')),
                ('sort', models.IntegerField(verbose_name='排序')),
                ('component', models.CharField(max_length=128, verbose_name='组件标识')),
                ('component_path', models.CharField(max_length=128, verbose_name='组件路径')),
                ('cache', models.BooleanField(default=False, verbose_name='keep-alive')),
                ('is_lock', models.BooleanField(default=False, verbose_name='锁定')),
            ],
            options={
                'db_table': 'msk_route',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='user_role',
            field=models.ManyToManyField(db_table='user_to_role', to='user.Role', verbose_name='用户角色'),
        ),
    ]
