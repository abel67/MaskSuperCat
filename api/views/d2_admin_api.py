#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-4-8 下午2:50
# @Author  : abel
# @Email   : abel@foolcat.cn
# @File    : d2_admin_api.py
# @Software: PyCharm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from user.models import Menu, Route, Interface, Role, User
from api.views._common import Common, CustomViewBase, JsonResponse
from api.serializers import MenuSerializer, RouteSerializer, UserSerializer, UserAddSerializer, \
    RoleSerializer, InterfaceSerializer, RolesPermissionsSerializers

from django.db.models import F
import datetime


class Login(APIView):

    @staticmethod
    def post(request):
        """
        用于用户登录，账号密码效验
        :param request:
        :return:
        """
        if not request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user_info = User.objects.filter(name=request.data["username"],
                                        password=request.data["password"]).values("id", "name", "true_name").first()
        if user_info:
            token_str = Token.objects.get(user=user_info['id']).key
            request.user = user_info["name"]
            user_info['name'] = user_info.pop('true_name')
            user_info["id"] = str(user_info["id"])
            return JsonResponse(code=status.HTTP_200_OK, token=token_str, data=user_info)
        else:
            return JsonResponse(code=499, msg="用户名或密码错误", data=user_info)


class Menus(Common, CustomViewBase):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        data = Common._list_data(self, self.queryset)
        return JsonResponse(code=status.HTTP_200_OK, data=data, ret_status=status.HTTP_200_OK)


class Routes(Common, CustomViewBase):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        data = Common._list_data(self, self.queryset)
        return JsonResponse(code=status.HTTP_200_OK, data=data, ret_status=status.HTTP_200_OK)


class Users(Common, CustomViewBase, ):
    """ 用户相关视图类[分页，增删改查]"""
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def paged(self, request):
        """
        分页方法
        :param request:
        :return:
        """
        queryset = User.objects.all().order_by("id")
        data = Common._paged(self, serializer_class=self.serializer_class, request=request, queryset=queryset)
        return JsonResponse(code=status.HTTP_200_OK, ret_status=status.HTTP_200_OK, data=data)

    def info(self, request):
        """
        用户已经登陆后，get时获取的数据
        :param request:
        :return:
        """
        username = request.user.name
        user_code = request.user.is_superuser
        role_list = self._user_role(username)
        permissions_list, access_menus = self._menus(role_list, user_code)
        # access_routes = self._routes(role_list, user_code)
        access_routes = self._routes()

        access_interfaces = self._interfaces(role_list, user_code)

        data = {"userName": username, "isAdmin": user_code, "userRoles": role_list,
                "userPermissions": permissions_list,
                "accessMenus": access_menus, "accessRoutes": access_routes, "accessInterfaces": access_interfaces,
                "avatarUrl": "https://api.adorable.io/avatars/85/abott@adorable.png"
                }
        return JsonResponse(code=status.HTTP_200_OK, data=data)

    def role_to_user(self, request):
        """
        角色与用户关系绑定
        :param request:
        :return:
        """
        action = request.data["action"]
        user_id = request.data["user_id"]
        role_id = request.data["role_id"]
        user = self.queryset.filter(id=user_id).first()
        if action:
            user.user_role.add(role_id)
        else:
            user.user_role.remove(role_id)
        return JsonResponse(code=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        新增用户时，新增token
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request.data["create_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        request.data["last_login"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        serializer_class = UserAddSerializer(data=request.data)
        if serializer_class.is_valid():
            name = serializer_class.save()
            if name:
                Token.objects.create(user=name)
                return JsonResponse(code=status.HTTP_200_OK)

        else:
            data = serializer_class.errors
            return JsonResponse(code=status.HTTP_200_OK, data=data)

    @staticmethod
    def batch_del(request):
        id_list = Common._json(request.GET.get("ids"))
        User.objects.filter(pk__in=id_list).delete()
        return JsonResponse(code=status.HTTP_200_OK)

    @staticmethod
    def _user_role(username):
        """
        获取传入用户所属的所有角色
        :param username: 已登录用户的用户名
        :return: ["user_role_1","user_role_2"...]
        """
        role_query = User.objects.filter(name=username).values("user_role__code").all()
        role_list = [role['user_role__code'] for role in role_query if role["user_role__code"]]
        return role_list

    def _menus(self, role_code_list: list, user_code):
        """
        获取传入所有角色的所有权限
        :param role_code_list: ["user_role_1", "user_role_2", ...]
        :return: ["permissions_name1", "permissions_name2", ...]
        """
        all_menus = []
        permissions_list = []
        first_menus = []
        if user_code:
            menu_queryset = Menu.objects.all().values().order_by('sort')
            self._menu_queryset(menu_queryset, all_menus, permissions_list, first_menus)
        else:
            for role_code in role_code_list:
                menu_queryset = Menu.objects.filter(role__code=role_code).all().values().order_by('sort')
                self._menu_queryset(menu_queryset, all_menus, permissions_list, first_menus)
        access_menus = self._parent_all(first_menus, all_menus)
        return permissions_list, access_menus

    @staticmethod
    def _menu_queryset(menu_queryset, all_menus, permissions_list, first_menus):
        """
        根据传入的menu_queryset,返回相应的数据
        :param menu_queryset: menu_queryset
        :return: first_menus, all_menus, permissions_list
        """

        for menu_dict in menu_queryset:
            # 去除用户有多个角色,会导入同一菜单的情况
            if menu_dict in first_menus:
                continue
            if menu_dict['type'] == 1:
                if menu_dict['parent_id'] == 0:
                    first_menus.append(menu_dict)
                all_menus.append(menu_dict)
            if menu_dict['permission'] in permissions_list:
                continue
            permissions_list.append(menu_dict['permission'])
        return first_menus, all_menus, permissions_list

    def _routes(self):
        all_routes = []
        first_routes = []
        # if user_code:
        route_queryset = Route.objects.all().values()
        self._route_queryset(route_queryset, first_routes, all_routes)
        # else:
        #     for role_code in role_code_list:
        #         route_queryset = Route.objects.filter(role__code=role_code).all().values()
        #         self._route_queryset(route_queryset, first_routes, all_routes)
        access_routes = self._parent_all(first_routes, all_routes, method=True)
        return access_routes

    @staticmethod
    def _route_queryset(route_queryset, first_routes, all_routes):
        for route_dict in route_queryset:
            # 去除用户有多个角色,会导入同一菜单的情况
            if route_dict in all_routes:
                continue
            if route_dict['parent_id'] == 0:
                first_routes.append(route_dict)
            all_routes.append(route_dict)
        return first_routes, all_routes

    def _interfaces(self, role_code_list, user_code):
        interfaces_list = []
        if user_code:
            interfaces_queryset = Interface.objects.filter().all().values()
            self._interfaces_queryset(interfaces_queryset, interfaces_list)
        else:
            for role_code in role_code_list:
                interfaces_queryset = Interface.objects.filter(menu__role__code=role_code).all().values()
                self._interfaces_queryset(interfaces_queryset, interfaces_list)
        return interfaces_list

    @staticmethod
    def _interfaces_queryset(interfaces_queryset, interfaces_list):
        """
        根据传入的interfaces_queryset,返回相应的数据,返回相应的数据
        :param interfaces_queryset:
        :param interfaces_list:
        :return:
        """
        for interfaces_dict in interfaces_queryset:
            # 去除用户有多个角色,会导入同一菜单的情况
            if interfaces_dict in interfaces_list:
                continue
            interfaces_list.append(interfaces_dict)
        return interfaces_list


class Roles(Common, CustomViewBase):
    """角色列表分页"""
    queryset = Role.objects.all().order_by("id")
    serializer_class = RoleSerializer
    permission_classes = (IsAuthenticated,)

    def paged(self, request):
        # 过滤
        queryset = Role.objects.all().order_by("id")
        data = Common._paged(self, serializer_class=self.serializer_class, request=request, queryset=queryset)
        return JsonResponse(code=status.HTTP_200_OK, ret_status=status.HTTP_200_OK, data=data)

    @staticmethod
    def batch_del(request):
        id_list = Common._json(request.GET.get("ids"))
        Role.objects.filter(pk__in=id_list).delete()
        return JsonResponse(code=status.HTTP_200_OK)


class RolesPermissions(Common, CustomViewBase):
    queryset = Role.objects.all().order_by("id")
    serializer_class = RolesPermissionsSerializers
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        pk = request.path.split("/")[-2]
        data = Role.objects.filter(id=pk, menus__type=2).annotate(role_id=F("id"), functionId=F("menus__id")).values(
            "role_id", "functionId")
        return JsonResponse(code=status.HTTP_200_OK, ret_status=status.HTTP_200_OK, data=data)

    def create(self, request, *args, **kwargs):
        role_id = request.data["role_id"]
        req_menus = request.data["permissions"]
        role = Role.objects.filter(id=role_id).first()
        all_menus = Menu.objects.all().values("id", "parent_id")
        ret_menus = self._relyon_all(id_lists=req_menus, all_data=all_menus, abc=[])
        try:
            role.menus.set(ret_menus)
            return JsonResponse(code=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse(code=status.HTTP_403_FORBIDDEN, data=e)


class InterFaces(Common, CustomViewBase):
    queryset = Interface.objects.all().order_by("id")
    serializer_class = InterfaceSerializer
    permission_classes = (IsAuthenticated,)

    def paged(self, request):
        """
        :param request:
        :return:
        """

        queryset = Interface.objects.all().order_by("id")
        data = Common._paged(self, serializer_class=self.serializer_class, request=request, queryset=queryset)
        return JsonResponse(code=status.HTTP_200_OK, ret_status=status.HTTP_200_OK, data=data)

    def api_to_menu(self, request):
        """
        角色与用户关系绑定
        :param request:
        :return:
        """
        action = request.data["action"]
        menu_id = request.data["functionId"]
        interface = self.queryset.filter(id=request.data["interfaceId"]).first()
        if action:
            interface.menu_set.add(menu_id)
        else:
            interface.menu_set.remove(menu_id)
        return JsonResponse(code=status.HTTP_200_OK)

    @staticmethod
    def batch_del(request):
        """
        根据传入的ids列表,批量删除msk_interface内对应id的数据
        :param request:
        :return:
        """
        id_list = Common._json(request.GET.get("ids"))
        Interface.objects.filter(pk__in=id_list).delete()
        return JsonResponse(code=status.HTTP_200_OK)
