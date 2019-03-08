from django.db import models

# Create your models here.


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=18, unique=True, verbose_name="用户名")
    password = models.CharField(max_length=78, verbose_name="用户密码")
    email = models.EmailField(max_length=128, verbose_name="用户邮箱")
    create_date = models.DateTimeField(verbose_name="创建日期")
    last_login = models.DateTimeField(verbose_name="最后登录")
    is_superuser = models.CharField(max_length=2, choices=((1, u'是'), (2, u'否')), verbose_name="超级用户")
    true_name = models.CharField(max_length=8, verbose_name="激活状态")
    user_role = models.ManyToManyField("Role", db_table="user_to_role", verbose_name="用户角色")

    class Meta:
        db_table = "msk_users"


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=18, unique=True, verbose_name="角色名")
    code = models.CharField(max_length=128, verbose_name="角色代码")
    description = models.CharField(max_length=128, verbose_name="角色描述")
    permission = models.ManyToManyField('Menu', db_table='role_to_menu', verbose_name="角色权限")

    class Meta:
        db_table = "msk_role"


class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    parent_id = models.CharField(max_length=128, verbose_name="父节点ID")
    path = models.CharField(max_length=128, verbose_name="菜单路径")
    title = models.CharField(max_length=128, verbose_name="菜单标题")
    icon = models.CharField(max_length=128, verbose_name="菜单图标")
    permission = models.CharField(max_length=128, verbose_name="菜单权限标识")
    type = models.CharField(max_length=2, choices=((0, u"菜单"), (1, "功能")), verbose_name="类型")
    sort = models.IntegerField(verbose_name="排序")
    is_lock = models.BooleanField(default=False, verbose_name="锁定")
    api = models.ManyToManyField('Interface', db_table='menu_to_interface')

    class Meta:
        db_table = "msk_menu"


class Interface(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=18, unique=True, verbose_name="接口名")
    path = models.CharField(max_length=128, verbose_name="接口路径")
    method = models.CharField(max_length=8, verbose_name="调用方法")
    description = models.CharField(max_length=128,verbose_name="接口描述")

    class Meta:
        db_table = "msk_interface"


class Route(models.Model):
    id = models.AutoField(primary_key=True)
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
