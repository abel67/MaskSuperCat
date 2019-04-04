#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-3-14 上午11:05
# @Author  : abel
# @Email   : abel@foolcat.cn
# @File    : user_api.py
# @Software: PyCharm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.models import User
from user.models import Menu, Route, Interface
from api.views._common import Common, JsonResponse
from rest_framework.authtoken.models import Token


class UserInfo(Common, APIView):
    """
    {
      "statusCode": 200,
      "msg": "",
      "data": {
        "userName": "",
        "isAdmin": 0,
        "userRoles": [],
        "userPermissions": [],
        "accessMenus": [],
        "accessRoutes": [],
        "accessInterfaces": [],
        "avatarUrl": "https://api.adorable.io/avatars/85/abott@adorable.png"
      }
    }
    """

    def get(self, request):
        data = {}
        req_token = request.META.get('HTTP_AUTHORIZATION')
        if req_token:
            # 根据token获取user
            token = req_token.split()[1].strip()
            username = Token.objects.get(key=token).user.username
            user_code = Token.objects.get(key=token).user.is_superuser
            role_list = self._user_role(username)
            permissions_list, access_menus = self.menus(role_list)
            access_routes = self.routes(role_list)
            access_interfaces = self.interfaces(role_list)
            data = {"userName": username, "isAdmin": user_code, "userRoles": role_list,
                    "userPermissions": permissions_list,
                    "accessMenus": access_menus, "accessRoutes": access_routes, "accessInterfaces": access_interfaces, "avatarUrl": ""
                    }
            return JsonResponse(code=status.HTTP_200_OK,data=data)
        return Response(data)

    @staticmethod
    def _user_role(username):
        """
        获取传入用户所属的所有角色
        :param username: 已登录用户的用户名
        :return: ["user_role_1","user_role_2"...]
        """
        role_query = User.objects.filter(username=username).values("user_role__code").all()
        role_list = [role['user_role__code'] for role in role_query if role["user_role__code"]]
        return role_list

    def menus(self, role_code_list: list):
        """
        获取传入所有角色的所有权限
        :param role_code_list: ["user_role_1", "user_role_2", ...]
        :return: ["permissions_name1", "permissions_name2", ...]
        """
        menu_list = []
        permissions_list = []
        first_menus = []
        for role_code in role_code_list:
            menu_queryset = Menu.objects.filter(role__code=role_code).all().values().order_by('sort')
            for menu_dict in menu_queryset:
                # 去除用户有多个角色,会导入同一菜单的情况
                if menu_dict in first_menus:
                    continue
                if menu_dict['type'] == 1:
                    if menu_dict['parentId'] == 0:
                        first_menus.append(menu_dict)
                    menu_list.append(menu_dict)
                permissions_list.append(menu_dict['permission'])
        else:
            access_menus = self._parentAll(first_menus, menu_list)
        return permissions_list, access_menus

    def routes(self, role_code_list: list):
        route_list = []
        first_route = []
        for role_code in role_code_list:
            route_queryset = Route.objects.filter(role__code=role_code).all().values()
            for route_dict in route_queryset:
                # 去除用户有多个角色,会导入同一菜单的情况
                if route_dict in first_route:
                    continue
                if route_dict['parentId'] == 0:
                    first_route.append(route_dict)
                route_list.append(route_dict)
        else:
            access_routes = self._parentAll(first_route, route_list)
        return access_routes

    def interfaces(self, role_code_list):
        interfaces_list = []
        for role_code in role_code_list:
            interfaces_queryset = Interface.objects.filter(menu__role__code=role_code).all().values()
            for interfaces_dict in interfaces_queryset:
                # 去除用户有多个角色,会导入同一菜单的情况
                if interfaces_dict in interfaces_list:
                    continue
                interfaces_list.append(interfaces_dict)
        return interfaces_list




# class Users(Common, CustomViewBase):
#
#     queryset = Menu.objects.all()
#     serializer_class = MenuSerializer
#
#     def list(self, request, *args, **kwargs):
#         menu_list = []
#         first_menus = []
#         menu_queryset = Menu.objects.all().values().order_by('sort')
#         for menu_dict in menu_queryset:
#             # 去除用户有多个角色,会导入同一菜单的情况
#             if menu_dict in first_menus:
#                 continue
#             if menu_dict['parentId'] == 0:
#                 first_menus.append(menu_dict)
#             menu_list.append(menu_dict)
#         else:
#             access_menus = self._parentAll(first_menus, menu_list)
#         return JsonResponse(code=status.HTTP_200_OK, data=access_menus, status=status.HTTP_200_OK)