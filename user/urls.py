# -*- coding: utf-8 -*-
# @Time    : 19-3-7 下午6:46
# @Author  : Mat
# @Email   : mat_wu@163.com
# @File    : urls.py
# @Software: PyCharm
from django.urls import path,re_path
from . import views

# 路由结构
urlpatterns = [
    path('login/', views.login),
]