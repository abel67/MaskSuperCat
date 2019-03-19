#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-3-13 下午2:00
# @Author  : abel
# @Email   : abel@foolcat.cn
# @File    : urls.py
# @Software: PyCharm

from django.urls import path, include
from api.views import (authentication_api,user_api)

from rest_framework.authtoken import views



# 使用自动URL路由连接我们的API。
# 另外，我们还包括支持浏览器浏览API的登录URL。
urlpatterns = [
    path('auth/login/', authentication_api.Login.as_view()),
    path('user/info/', user_api.UserInfo.as_view()),
]