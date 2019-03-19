from django.shortcuts import render, HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.middleware import csrf
from django.views.decorators.csrf import csrf_exempt
import json
from . import models

# 返回的code与状态
ret_status = {'methodError': {'retcode': 500, 'status': 'methodError'},
          'failed': {'retcode': 400, 'status': 'failed'},
          "success": {'statusCode': 200,"msg": ""},
        "notFound": {'retcode': 404, 'status': 'Not Found'}}

# Create your views here.


# @csrf_exempt
# def login(request):
#     """
#     用户登录方法
#     :param request:
#     :return: {"statusCode": 200 , "data":{"accessToken": "" ,"id": 1 , "name": "admin"}}
#     """
#
#     try:
#         user_form = json.loads(request.body)
#         csrftoken = csrf.get_token(request)
#         user_info = models.User.objects.filter(name=user_form["username"], password=user_form["password"]). \
#             values('id',"name").first()
#         user_info['accessToken'] = csrftoken
#         ret_status['success']['data'] = user_info
#     except Exception as e:
#         pass
#     return JsonResponse(ret_status['success'])

def info(request):
    """
    获取当前用户信息
    :param request:
    :return:
    """

    return JsonResponse(ret_status['success'])


    # if request.method == 'GET':
    #     return render(request, 'web/login.html')
    # else:
    #     name = request.POST.get("name")
    #     password = request.POST.get("password")
    #     # # 根据用户名在数据库内查询数据
    #     query_user = models.Users.objects.filter(name=name).first()
