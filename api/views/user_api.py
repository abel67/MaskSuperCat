#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-3-14 上午11:05
# @Author  : abel
# @Email   : abel@foolcat.cn
# @File    : user_api.py
# @Software: PyCharm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.models import User
from user.models import Role,Menu

from api.serializers import UserInfoSerializer
from api.views._common import _http_result
from rest_framework.authtoken.models import Token


class UserInfo(APIView):

	def get(self, request):
		data = {}
		req_token =  request.META.get('HTTP_AUTHORIZATION')
		if req_token:
			# 根据token获取user
			token = req_token.split()[1].strip()
			username = Token.objects.get(key=token).user.username
			user_code = Token.objects.get(key=token).user.is_superuser
			role_list = self._user_role(username)
			menu_data = self._menus(role_list)
			accessMenus = self._accessMenus(menu_data)
			return Response(data)
		return Response(data)

	def _user_role(self, username):
		"""
		获取传入用户所属的所有角色
		:param username: 已登录用户的用户名
		:return: ["user_role_1","user_role_2"...]
		"""
		role_query = User.objects.filter(username=username).values("user_role__code").all()
		role_list = [ role['user_role__code'] for role in role_query if role["user_role__code"]]
		return role_list

	def _menus(self, role_code_list: list):
		"""
		获取传入所有角色的所有权限
		:param role_code_list: ["user_role_1", "user_role_2", ...]
		:return: ["permissions_name1", "permissions_name2", ...]
		"""
		menu_list = []
		permissions_list = []
		first_menu = []
		menu_node =set()
		for role_code in role_code_list:
			menu_queryset = Menu.objects.filter(role__code=role_code).all().values()
			for menu_dict in menu_queryset:
				if menu_dict['parent_id'] == '0':
					first_menu.append(menu_dict)
				if menu_dict['type'] == 0 :
					menu_node.add(menu_dict['parent_id'])
					menu_list.append({menu_dict['parent_id']:menu_dict})
				permissions_list.append(menu_dict['permission'])
		menu_data = {"menu_node":menu_node, "menu_list":menu_list,"permissions_list":permissions_list,"first_menu":first_menu}
		return menu_data

	def _accessMenus(self ,menu_data):
		print(menu_data)
		for first_menu in menu_data["first_menu"]:
			children = []
			for node in menu_data["menu_node"]:
				if first_menu["parent_id"]  == node :
					continue

			# print(menu_data['first_menu'][n][i])
		return menu_data

	# def _accessMenus(self,permissions_list):
	# 	menu_list = []
	# 	for permission in permissions_list:
	# 		menu_quey = Menu.objects.filter(permission=permission).all().values()
	# 		for menu in menu_quey:
	# 			menu_list.append(menu)
	# 	print(menu_list)
	# 	return menu_list

"""
{
  "statusCode": 200,
  "msg": "",
  "data": {
    "userName": "",
    "isAdmin": 0,
    "userRoles": [],
    "userPermissions": [],
    "accessMenus": [],
    "accessRoutes": [],
    "accessInterfaces": [],

    "avatarUrl": "https://api.adorable.io/avatars/85/abott@adorable.png"
  }
}
"""




class UserAdd(APIView):
	"""
	新增用户
	"""

	def post(self,request):
		pass


	def _addToken(self, user_info):
		"""

		:return:
		"""
		# user=model对象
		token = Token.objects.create(user=user_info)
		return token.key