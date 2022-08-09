#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/22 13:58
# @Name    : peilun
# @File    : logs_auth.py
# @Software: PyCharm
from flask import request, Blueprint
from comment.flask_apiauth import auth
from comment.db_manipulation import logs
import json


'''
   日志相关接口
'''
log = Blueprint('log', __name__)

# 获取最近一次构建记录
@log.route('jenkins/record', methods=['POST'])
@auth.login_required
def record():
    param = json.loads(request.data)
    cid = param['cid']
    userid = param['userid']
    username = param['username']
    content = param['content']

    if param is not None:
        data = logs.logings(cid, userid, username, content)
        return {
            'code': '200',
            'data': data,
            'message': '成功'
        }
    else:
        return {
            'code': '403',
            'data': {},
            'message': '参数不完整'
        }

# 查询所有日志信息
@log.route('api/logs/allquery', methods=['POST'])
@auth.login_required
def logallquery():
    param = json.loads(request.data)
    pageNum = param['pageNum']
    pageSize = param['pageSize']

    if param is not None:
        data = logs.logsall_query(pageNum, pageSize)
        return {
            'code': '200',
            'data': data,
            'message': '成功'
        }
    else:
        return {
            'code': '403',
            'data': {},
            'message': '参数不完整'
        }


# 根据operator_name 查询日志信息
@log.route('api/logs/query', methods=['POST'])
@auth.login_required
def logquery():
    param = json.loads(request.data)
    operator_name = param['operator_name']
    pageNum = param['pageNum']
    pageSize = param['pageSize']

    if param is not None:
        data = logs.logsname_query(operator_name, pageNum, pageSize)
        return {
            'code': '200',
            'data': data,
            'message': '成功'
        }
    else:
        return {
            'code': '403',
            'data': {},
            'message': '参数不完整'
        }