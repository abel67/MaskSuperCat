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

	def get(self, request):
		data = {}
		req_token =  request.META.get('HTTP_AUTHORIZATION')
		if req_token:
			# 根据token获取user
			token = req_token.split()[1].strip()
			username = Token.objects.get(key=token).user.username
			user_code = Token.objects.get(key=token).user.is_superuser
			role_list = self._user_role(username)
			permissions_list, first_menus, menu_list = self._menus(role_list)
			accessMenus = self._accessMenus(first_menus, menu_list)
			print(accessMenus)
			data = {"userName": username, "isAdmin": user_code, "userRoles": role_list,
					"userPermissions": permissions_list,
					"accessMenus": accessMenus, "accessRoutes": [], "accessInterfaces": [], "avatarUrl": ""
					}

			return Response(_http_result(status.HTTP_200_OK, data=data))
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
		first_menus =[]
		for role_code in role_code_list:
			menu_queryset = Menu.objects.filter(role__code=role_code).all().values()
			for menu_dict in menu_queryset:
				if menu_dict['type'] == 0 :
					if menu_dict['parent_id'] == '0':
						first_menus.append(menu_dict)
					menu_list.append(menu_dict)
				permissions_list.append(menu_dict['permission'])
		return permissions_list, first_menus, menu_list

	def _accessMenus(self, first_menus, menu_list):
		"""
		将用户有权限的菜单正合返回
		:param first_menus:
		:param menu_list:
		:return:
		"""
		print(first_menus)
		for node in first_menus:
			children = self._subMenus(node['menu_id'], menu_list)
			if children:
				# 如果有子菜单则继续递归执行
				node["children"] = children
				self._accessMenus(children, menu_list)
		else:
			return first_menus

	@staticmethod
	def _subMenus(parent_id, menu_list ):
		"""
		根据菜单id,获取所有的子菜单
		:param parent_id:
		:param menu_list:
		:return:
		"""
		sub_menus = []
		for menu in menu_list:
			if parent_id == menu["parent_id"]:
				sub_menus.append(menu)
		else:
			return sub_menus

	# def _accessMenus(self,permissions_list):
	# 	menu_list = []
	# 	for permission in permissions_list:
	# 		menu_quey = Menu.objects.filter(permission=permission).all().values()
	# 		for menu in menu_quey:
	# 			menu_list.append(menu)
	# 	print(menu_list)
	# 	return menu_list






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