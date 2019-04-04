#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-4-4 上午10:15
# @Author  : abel
# @Email   : abel@foolcat.cn
# @File    : menu_api.py
# @Software: PyCharm
from api.serializers import MenuSerializer
from user.models import Menu
from rest_framework import status
from ._common import Common, CustomViewBase, JsonResponse


class Menus(Common, CustomViewBase):

    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def list(self, request, *args, **kwargs):
        menu_list = []
        first_menus = []
        menu_queryset = Menu.objects.all().values().order_by('sort')
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