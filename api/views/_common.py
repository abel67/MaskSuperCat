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
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import BaseFilterBackend
from rest_framework import status, viewsets, filters
from django_filters import rest_framework
# from django.contrib.auth.models import AnonymousUser
import json


class JsonResponse(Response):
    """
    An HttpResponse that allows its data to be rendered into
    arbitrary media types.
    """

    def __init__(self, data=None, code=None, token=None, msg="", ret_status=None, template_name=None,
                 exception=False, content_type=None, headers=None):
        """
        Alters the init arguments slightly.
        For example, drop 'template_name', and instead use 'data'.
        Setting 'renderer' and 'media_type' will typically be deferred,
        For example being set automatically by the `APIView`.
        """
        super(Response, self).__init__(None, status=ret_status)

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
        return JsonResponse(data=serializer.data, msg="success", code=200, headers=headers,
                            ret_status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(data=serializer.data, code=200, msg="success", ret_status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return JsonResponse(data=serializer.data, code=200, msg="success", ret_status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        print("update")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        for key in request.data:
            # 将value内字符串为空的值替换为None, 否则会提交数据库失败
            if type(request.data[key]) == str and not request.data[key]:
                request.data[key] = None

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return JsonResponse(data=serializer.data, msg="success", code=200, ret_status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        print("destroy")
        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse(data=[], code=200, msg="delete resource success", ret_status=status.HTTP_200_OK)


class Common:

    @staticmethod
    def _json(metadata: str) -> json:
        json_data = json.loads(metadata)
        return json_data

    def _parent_all(self, parent_list, all_data, method=None):
        """
        将用户所有有权限的菜单或路由的字典嵌套的列表返回
        :param parent_list: 所有parent_id为0的
        :param all_data: 所有有权限的数据
        :return: [{"id": 1 , "children": [{"parent_id":1}]}]
        """
        for node in parent_list:
            if method:
                node["meta"] = {"title": node["title"], "cache": node["cache"]}
                node.pop("title"), node.pop("cache")
            children = self._sub_all(node['id'], all_data)
            if children:
                node["children"] = children
                # 如果有子菜单则继续递归执行
                self._parent_all(children, all_data, method)
        else:
            return parent_list

    @staticmethod
    def _sub_all(parent_id, all_data, ):
        """
        根据parent_id,获取所有的子菜单
        :param parent_id: 父ID
        :param all_data: 所有列表
        :return: [{menu1},{menu2}]
        """
        sub_list = []
        for data in all_data:
            if parent_id == data["parent_id"]:
                sub_list.append(data)
        else:
            return sub_list

    def _relyon_all(self, id_lists, all_data, abc):
        """

        :param id_lists:
        :param all_data:
        :param abc:
        :return:
        """
        parent_id_list = []
        for data_dict in all_data:
            if data_dict["id"] in id_lists:
                abc.append(data_dict["id"])
                parent_id_list.append(data_dict["parent_id"])
        else:
            if parent_id_list:
                self._relyon_all(parent_id_list, all_data, abc)
        return set(abc)

    @staticmethod
    def _paged(view, serializer_class, request, queryset):
        filter_data = MSKFilterBackend().filter_queryset(request=request, queryset=queryset, view=view)
        if filter_data["name"]:
            # 动态修改对象内变量值
            setattr(serializer_class, filter_data["name"], filter_data["id"])
        # 创建分页对象
        paged = MSKPagination()
        # 把数据放在分页器上面
        page_user_list = paged.paginate_queryset(queryset=filter_data["data"], request=request, view=view)

        ser = serializer_class(instance=page_user_list, many=True)  # 序列化数据
        data = {"totalCount": len(filter_data["data"]), "rows": ser.data}
        return data

    def _list_data(self, queryset):
        """
        :return:
        """
        all_data = []
        first_data = []
        route_queryset = queryset.values().order_by('sort')
        for route_dict in route_queryset:
            # 去除用户有多个角色,会导入同一菜单的情况
            if route_dict in first_data:
                continue
            if route_dict['parent_id'] == 0:
                first_data.append(route_dict)
            all_data.append(route_dict)
        else:
            all_data = self._parent_all(first_data, all_data)
        return all_data


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
        :return:
        """
        f_id = request.GET.get("id") if request.GET.get("id") else False
        f_name = "{}_id".format(request.GET.get("type")) if request.GET.get("type") else False
        filter_dict = self._filter(request.GET.get("filter"))

        filter_data = {"name": f_name, "id": f_id, "data": queryset.filter(**filter_dict)}
        return filter_data

    @staticmethod
    def _filter(f_params: json, f_type: str = None, f_id: str = None):
        """
        :param f_params:
        :param f_type:
        :param f_id:
        :return:
        """
        filter_dict = json.loads(f_params)

        # 去除空值,并使用模糊查询
        filter_dict = {"{}__contains".format(key): filter_dict[key] for key in filter_dict if filter_dict[key]}
        return filter_dict
