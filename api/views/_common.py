#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-3-13 下午4:48
# @Author  : abel
# @Email   : abel@foolcat.cn
# @File    : _common.py
# @Software: PyCharm

def _http_result(code: int, data: dict, token: str = "",  msg: str = "",) -> dict or bool:
    """
    自定义https返回的json
    :param code: int
    :param data: None or dict
    :param msg: str
    :return: dict or bool
    """
    try:
        if token:
            data["accessToken"] = token
        result = {"statusCode": code, "msg": msg, "data": data}
        return result
    except Exception as e:
        return False