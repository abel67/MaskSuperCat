#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-3-13 下午3:40
# @Author  : abel
# @Email   : abel@foolcat.cn
# @File    : login_api.py
# @Software: PyCharm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.models import User
from api.serializers import LoginSerializer
from ._common import JsonResponse
from rest_framework.authtoken.models import Token


class Login(APIView):

    def post(self, request):
        """
        用于用户登录，账号密码效验
        :param request:
        :return:
        """
        if not request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user_form = request.data
        user_info = User.objects.filter(username=user_form["username"], password=user_form["password"]).first()
        serializers = LoginSerializer(instance=user_info, data=user_form)
        if serializers.is_valid(raise_exception=True):
            token_str = Token.objects.get(user=serializers.data['id']).key
            return JsonResponse(code=status.HTTP_200_OK,token=token_str, data=serializers.data)
        else:
            return JsonResponse(code=499, msg="用户名或密码错误", data=serializers.data)