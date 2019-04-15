#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-3-11 下午5:46
# @Author  : abel
# @Email   : abel@foolcat.cn
# @File    : serializers.py
# @Software: PyCharm
from user.models import User, Role, Route, Menu, Interface
from rest_framework import serializers


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    roleId = None
    isAdd = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ("user_role", "create_time")
        ordering_fields = ('id',)

    def get_isAdd(self, obj):
        role_queryset = Role.objects.filter(user__name=obj.name, id=self.roleId)
        if role_queryset:
            is_add = 1
        else:
            is_add = 2
        return is_add


class UserAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ("user_role",)


class MenuSerializer(serializers.ModelSerializer):
    path = serializers.CharField(allow_null=True,label='路径', max_length=128, required=False)

    class Meta:
        model = Menu
        exclude = ('api',)
        ordering_fields = ('sort',)


class RouteSerializer(serializers.ModelSerializer):
    path = serializers.CharField(allow_null=True, label='路径', max_length=128, required=False)

    class Meta:
        model = Route
        fields = "__all__"
        # exclude = ('id', 'api')
        ordering_fields = ('id', 'sort')


class RoleSerializer(serializers.ModelSerializer):
    userId = None
    isAdd = serializers.SerializerMethodField()

    class Meta:
        model = Role
        exclude = ('menus',)

    def get_isAdd(self, obj):
        user_queryset = User.objects.filter(id=self.userId, user_role__id=obj.id)

        if user_queryset:
            is_add = 1
        else:
            is_add = 2
        return is_add

class RolesPermissionsSerializers(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ("id", "menus")




class InterfaceSerializer(serializers.ModelSerializer):
    menuId = None
    isAdd = serializers.SerializerMethodField()
    class Meta:
        model = Interface
        fields = "__all__"

    def get_isAdd(self, obj):
        menu_queryset = Menu.objects.filter(id=self.menuId, api__id=obj.id)
        print(menu_queryset)
        if menu_queryset:
            is_add = 1
        else:
            is_add = 2
        return is_add