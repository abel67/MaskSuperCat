from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    super_choices = (
        (0, '管理员'),
        (1, '普通用户'))
    is_superuser = models.SmallIntegerField(choices=super_choices)
    user_role = models.ManyToManyField("Role", db_table="user_to_role", verbose_name="用户角色")

    class Meta:
        db_table = "msk_user"


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=18, unique=True, verbose_name="角色名")
    code = models.CharField(max_length=128, null=True, verbose_name="角色代码")
    description = models.CharField(max_length=128, null=True, verbose_name="角色描述")
    permission = models.ManyToManyField('Menu', db_table='role_to_menu', verbose_name="角色权限")

    class Meta:
        db_table = "msk_role"


class Interface(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=18, unique=True, verbose_name="接口名")
    path = models.CharField(max_length=128, verbose_name="接口路径")
    method = models.CharField(max_length=8, verbose_name="调用方法")
    description = models.CharField(max_length=128, null=True, verbose_name="接口描述")

    class Meta:
        db_table = "msk_interface"





class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    menu_id = models.CharField(max_length=128, unique=True, verbose_name="菜单ID")
    parent_id = models.CharField(max_length=128, verbose_name="父菜单ID")
    path = models.CharField(max_length=128, verbose_name="菜单路径")
    title = models.CharField(max_length=128, verbose_name="菜单标题")
    icon = models.CharField(max_length=128, null=True, verbose_name="菜单图标")
    permission = models.CharField(max_length=128, null=True, verbose_name="菜单权限标识")
    type = models.CharField(max_length=2, choices=((0, u"菜单"), (1, "功能")), verbose_name="类型")
    sort = models.IntegerField(verbose_name="排序")
    is_lock = models.BooleanField(default=False, verbose_name="锁定")
    api = models.ManyToManyField('Interface', db_table='menu_to_interface')

    class Meta:
        db_table = "msk_menu"








class Route(models.Model):
    id = models.AutoField(primary_key=True)
    route_id = models.CharField(max_length=128, unique=True, verbose_name="路由ID")
    parent_id = models.CharField(max_length=128, verbose_name="父路由ID")
    path = models.CharField(max_length=128, verbose_name="路由路径")
    name = models.CharField(max_length=18, unique=True, verbose_name="路由名")
    title = models.CharField(max_length=128, verbose_name="路由标题")
    permission = models.CharField(max_length=128, verbose_name="路由权限标识")
    sort = models.IntegerField(verbose_name="排序")
    component = models.CharField(max_length=128, verbose_name="组件标识")
    component_path = models.CharField(max_length=128, verbose_name="组件路径")
    cache = models.BooleanField(default=False, verbose_name="keep-alive")
    is_lock = models.BooleanField(default=False, verbose_name="锁定")

    class Meta:
        db_table = "msk_route"


