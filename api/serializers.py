#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-3-11 下午5:46
# @Author  : abel
# @Email   : abel@foolcat.cn
# @File    : serializers.py
# @Software: PyCharm
from user.models import Role, Route, Menu
from user.models import User
from rest_framework import serializers


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name")


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    isAdd = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ("user_role","last_login","create_time")
        ordering_fields = ('id',)

    def get_isAdd(self, obj):
        role_queryset = Role.objects.filter(user__name=obj.name).all().first()
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
    class Meta:
        model = Menu
        exclude = ('api',)
        ordering_fields = ('sort',)


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = "__all__"
        # exclude = ('id', 'api')
        ordering_fields = ('id', 'sort')


class RoleSerializer(serializers.ModelSerializer):
    isAdd = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = "__all__"

    def get_isAdd(self, obj):
        print(obj.__dict__)
        # user_queryset = Role.objects.values("name").filter(user_role__code=obj.code)
        # print(user_queryset)
        # if is_add:
        #     is_add = 1
        # else:
        #     is_add = 2
        return "1"
