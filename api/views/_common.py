#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-3-13 下午4:48
# @Author  : abel
# @Email   : abel@foolcat.cn
# @File    : _common.py
# @Software: PyCharm
from django.utils import six
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import BaseFilterBackend
from rest_framework import status, viewsets, filters
from django_filters import rest_framework
from django.contrib.auth.models import AnonymousUser
import json


class JsonResponse(Response):
    """
    An HttpResponse that allows its data to be rendered into
    arbitrary media types.
    """

    def __init__(self, data=None, code=None, token=None, msg="", status=None, template_name=None, headers=None,
                 exception=False, content_type=None):
        """
        Alters the init arguments slightly.
        For example, drop 'template_name', and instead use 'data'.
        Setting 'renderer' and 'media_type' will typically be deferred,
        For example being set automatically by the `APIView`.
        """
        super(Response, self).__init__(None, status=status)

        if isinstance(data, Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(msg)
        if token:
            data["accessToken"] = token
        self.data = {"statusCode": code, "msg": msg, "data": data}
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in six.iteritems(headers):
                self[name] = value


class CustomViewBase(viewsets.ModelViewSet):
    queryset = ''
    serializer_class = ''
    permission_classes = ()
    filter_fields = ()
    search_fields = ()
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)

    def create(self, request, *args, **kwargs):
        print("create")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return JsonResponse(data=serializer.data, msg="success", code=200, status=status.HTTP_200_OK,
                            headers=headers)

    def list(self, request, *args, **kwargs):
        print("list")
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(data=serializer.data, code=200, msg="success", status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return JsonResponse(data=serializer.data, code=200, msg="success", status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        print("update")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return JsonResponse(data=serializer.data, msg="success", code=200, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        print("destroy")
        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse(data=[], code=200, msg="delete resource success", status=status.HTTP_200_OK)


class Common:

    def _parentAll(self, parent_list, all_data, method=None):
        """
        将用户所有有权限的菜单或路由的字典嵌套的列表返回
        :param parent_list: 所有parent_id为0的
        :param all_data: 所有有权限的数据
        :return: [{"id": 1 , "children": [{"parentId":1}]}]
        """
        for node in parent_list:
            if method:
                node["meta"] = {"title": node["title"], "cache": node["cache"]}
                node.pop("title"), node.pop("cache")
            children = self._subAll(node['id'], all_data)
            if children:
                node["children"] = children
                # 如果有子菜单则继续递归执行
                self._parentAll(children, all_data, method)
        else:
            return parent_list

    @staticmethod
    def _subAll(parent_id, all_data, ):
        """
        根据parent_id,获取所有的子菜单
        :param parent_id: 父ID
        :param all_data: 所有列表
        :return: [{menu1},{menu2}]
        """
        sub_list = []
        for data in all_data:
            if parent_id == data["parentId"]:
                sub_list.append(data)
        else:
            return sub_list

    def _relyonAll(self, id_lists, all_data, abc):
        parentId_list = []
        for data_dict in all_data:
            if data_dict["id"] in id_lists:
                abc.append(data_dict["id"])
                parentId_list.append(data_dict["parentId"])
        else:
            if parentId_list:
                self._relyonAll(parentId_list, all_data, abc)
        return set(abc)


class MSKPagination(PageNumberPagination):
    # 关键字
    page_size_query_param = 'pageSize'
    # max_page_size = 1  # 每页最多显示多少个
    # 页码
    page_query_param = 'pageIndex'  # 页码是从1开始的，也是关键字


class MSKFilterBackend(BaseFilterBackend):
    """
    自定义filter方法, 根据传入的值，返回filter后的queryset
    """

    def filter_queryset(self, request, queryset, view):
        """
        根据传值，返回相应的queryset
        :param request:
        :param queryset:
        :param view:
        :return:
        """
        if "interface" in request.path:
            filter_dict = self._interface(request, view)
        elif "role" in request.path or "user" in request.path:
            filter_dict = self.__role_user(request, view)
        else:
            return queryset
        return queryset.filter(**filter_dict)

    def _interface(self, request, view):
        """
        对接口进行过滤
        :param request:
        :param view:
        :return:
        """
        filter_dict = {"name": request.GET.get("name"), "path": request.GET.get("path"),
                       "method": request.GET.get("method")}
        if request.GET.get("functionId"):
            view.menuId = request.GET.get("functionId")
        filter_dict = {"{}__contains".format(key): filter_dict[key] for key in filter_dict if filter_dict[key]}
        return filter_dict

    def __role_user(self, request, view):
        """
        用户与角色过滤
        :param request:
        :param view:
        :return:
        """
        filter_params = request.GET.get("filter")
        filter_dict = json.loads(filter_params)
        if filter_dict.get("roleId"):
            view.roleId = filter_dict.pop("roleId")
        if filter_dict.get("userId"):
            view.userId = filter_dict.pop("userId")
        # 去除空值,并使用模式查询
        filter_dict = {"{}__contains".format(key): filter_dict[key] for key in filter_dict if filter_dict[key]}
        return filter_dict
