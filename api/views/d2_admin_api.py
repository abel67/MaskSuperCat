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
from user.models import User
from user.models import Menu, Route, Interface, Role
from api.views._common import Common, CustomViewBase, JsonResponse, MSKPagination
from api.serializers import LoginSerializer, MenuSerializer, RouteSerializer, UserSerializer, UserAddSerializer, \
    RoleSerializer
from rest_framework.authtoken.models import Token
import datetime


class Login(APIView):
    """
    登录方法
    """

    def post(self, request):
        """
        用于用户登录，账号密码效验
        :param request:
        :return:
        """
        if not request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user_info = User.objects.filter(name=request.data["username"],
                                        password=request.data["password"]).values("id", "trueName").first()
        if user_info:
            token_str = Token.objects.get(user=user_info['id']).key
            user_info['name'] = user_info.pop('trueName')
            return JsonResponse(code=status.HTTP_200_OK, token=token_str, data=user_info)
        else:
            return JsonResponse(code=499, msg="用户名或密码错误", data=user_info)


class Menus(Common, CustomViewBase):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def list(self, request, *args, **kwargs):
        menu_list = []
        first_menus = []
        menu_queryset = self.queryset.values().order_by('sort')
        for menu_dict in menu_queryset:
            # 去除用户有多个角色,会导入同一菜单的情况
            if menu_dict in first_menus:
                continue
            if menu_dict['parentId'] == 0:
                first_menus.append(menu_dict)
            menu_list.append(menu_dict)
        else:
            access_menus = self._parentAll(first_menus, menu_list)
        return JsonResponse(code=status.HTTP_200_OK, data=access_menus, status=status.HTTP_200_OK)


class Routes(Common, CustomViewBase):
    """

    """
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def list(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        all_routes = []
        first_routes = []
        route_queryset = self.queryset.values().order_by('sort')
        for route_dict in route_queryset:
            # 去除用户有多个角色,会导入同一菜单的情况
            if route_dict in first_routes:
                continue
            if route_dict['parentId'] == 0:
                first_routes.append(route_dict)
            all_routes.append(route_dict)
        else:
            access_routes = self._parentAll(first_routes, all_routes)
        return JsonResponse(code=status.HTTP_200_OK, data=access_routes, status=status.HTTP_200_OK)


class Users(Common, CustomViewBase):
    """ 用户相关视图类[分页，增删改查]"""
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer

    def paged(self, request):
        """
        分页方法
        :param request:
        :return:
        """
        # 创建分页对象
        queryset = User.objects.all().order_by("id")
        paged = MSKPagination()
        page_user_list = paged.paginate_queryset(queryset=queryset, request=request, view=self)  # 把数据放在分页器上面

        ser = self.serializer_class(instance=page_user_list, many=True)  # 序列化数据
        data = {"totalCount": len(queryset), "rows": ser.data}
        return JsonResponse(code=status.HTTP_200_OK, status=status.HTTP_200_OK, data=data)

    def info(self, request):
        """
        用户已经登陆后，get时获取的数据
        :param request: 主要获取用户的token
        :return:
        """
        data = {}
        req_token = request.META.get('HTTP_AUTHORIZATION')
        if req_token:
            # 根据token获取user
            token = req_token.split()[1].strip()
            username = Token.objects.get(key=token).user.name
            user_code = Token.objects.get(key=token).user.is_superuser
            role_list = self._user_role(username)
            permissions_list, access_menus = self._menus(role_list, user_code)
            access_routes = self._routes(role_list, user_code)
            access_interfaces = self._interfaces(role_list)
            data = {"userName": username, "isAdmin": user_code, "userRoles": role_list,
                    "userPermissions": permissions_list,
                    "accessMenus": access_menus, "accessRoutes": access_routes, "accessInterfaces": access_interfaces,
                    "avatarUrl": ""
                    }
        return JsonResponse(code=status.HTTP_200_OK, data=data)

    def role_to_user(self, request):
        """
        角色与用户关系绑定
        :param request:
        :return:
        """
        action = request.data["action"]
        user_id = request.data["userId"]
        role_id = request.data["roleId"]
        user = User.objects.filter(id=user_id).first()
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
                return JsonResponse(code=status.HTTP_200_OK, data=name)

        else:
            data = serializer_class.errors
            return JsonResponse(code=status.HTTP_200_OK, data=data)

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
        access_menus = self._parentAll(first_menus, all_menus)
        return permissions_list, access_menus

    def _menu_queryset(self, menu_queryset, all_menus, permissions_list, first_menus):
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
                if menu_dict['parentId'] == 0:
                    first_menus.append(menu_dict)
                all_menus.append(menu_dict)
            if menu_dict['permission'] in permissions_list:
                continue
            permissions_list.append(menu_dict['permission'])
        return first_menus, all_menus, permissions_list

    def _routes(self, role_code_list: list, user_code):
        all_routes = []
        first_routes = []
        if user_code:
            route_queryset = Route.objects.all().values()
            self._route_queryset(route_queryset, first_routes, all_routes)
        else:
            for role_code in role_code_list:
                route_queryset = Route.objects.filter(role__code=role_code).all().values()
                self._route_queryset(route_queryset, first_routes, all_routes)
        access_routes = self._parentAll(first_routes, all_routes)
        return access_routes

    def _route_queryset(self, route_queryset, first_routes, all_routes):

        for route_dict in route_queryset:
            # 去除用户有多个角色,会导入同一菜单的情况
            if route_dict in all_routes:
                continue
            if route_dict['parentId'] == 0:
                first_routes.append(route_dict)
            all_routes.append(route_dict)
        return first_routes, all_routes

    def _interfaces(self, role_code_list):
        interfaces_list = []
        for role_code in role_code_list:
            interfaces_queryset = Interface.objects.filter(menu__role__code=role_code).all().values()
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

    def paged(self, request):
        queryset = Role.objects.all().order_by("id")

        # 创建分页对象
        paged = MSKPagination()
        # 把数据放在分页器上面
        page_user_list = paged.paginate_queryset(queryset=queryset, request=request, view=self)
        ser = self.serializer_class(instance=page_user_list, many=True)  # 序列化数据
        data = {"totalCount": len(queryset), "rows": ser.data}
        return JsonResponse(code=status.HTTP_200_OK, status=status.HTTP_200_OK, data=data)
