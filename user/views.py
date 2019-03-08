from django.shortcuts import render,HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.middleware import csrf
from django.views.decorators.csrf import csrf_exempt
import json
from . import models

# Create your views here.
@csrf_exempt
def login(request):
    """
    用户登录方法
    :param request:
    :return: json格式的状态吗
    """
    try:
        user_info = json.loads(request.body)
    except Exception as e:
        pass
    print(user_info)
    csrftoken = csrf.get_token(request)

    return JsonResponse({"status": 200})

    # if request.method == 'GET':
    #     return render(request, 'web/login.html')
    # else:
    #     name = request.POST.get("name")
    #     password = request.POST.get("password")
    #     # # 根据用户名在数据库内查询数据
    #     query_user = models.Users.objects.filter(name=name).first()