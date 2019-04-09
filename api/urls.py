#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-3-13 下午2:00
# @Author  : abel
# @Email   : abel@foolcat.cn
# @File    : urls.py
# @Software: PyCharm

from django.urls import path, include
from api.views import (d2_admin_api)
from rest_framework import routers
from api.views.d2_admin_api import Menus, Routes, Users

router = routers.DefaultRouter()
router.register(r'menu', Menus)
router.register(r'route', Routes)
router.register(r'user', Users)
# 使用自动URL路由连接我们的API。
# 另外，我们还包括支持浏览器浏览API的登录URL。
urlpatterns = [
    path('auth/login/', d2_admin_api.Login.as_view()),
    path('user/info/', d2_admin_api.UserInfo.as_view()),
    path('user/pagedlist/', d2_admin_api.UserPaged.as_view()),
    path('role/pagedlist', d2_admin_api.RolePaged.as_view()),
    path('', include(router.urls)),
]


