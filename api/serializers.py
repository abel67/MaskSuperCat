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
        fields = ("id", "username")


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        exclude = ('id', 'api')
        ordering_fields = ('id', 'sort')