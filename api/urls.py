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
from api.views.d2_admin_api import Menus, Routes, Users, Roles

router = routers.DefaultRouter()
router.register(r'menu', Menus)
router.register(r'route', Routes)
router.register(r'user', Users)
# 使用自动URL路由连接我们的API。
# 另外，我们还包括支持浏览器浏览API的登录URL。
urlpatterns = [
    path('auth/login/', d2_admin_api.Login.as_view()),
    path('user/info/', Users.as_view({'get': 'info'})),
    path('user/pagedlist/', Users.as_view({'get': 'paged'})),
    path('user/editroleuser/', Users.as_view({'post': 'role_to_user'})),
    path('role/pagedlist', Roles.as_view({'get': 'paged'})),
    path('', include(router.urls)),
]


