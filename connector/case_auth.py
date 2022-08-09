#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/2 15:00
# @Name    : peilun
# @File    : case_auth.py
# @Software: PyCharm

from flask import request, Blueprint
from comment.flask_apiauth import auth
from comment.db_manipulation import cases, logs
from comment.log import log
import json

case = Blueprint('case', __name__)

'''
    用例接口
'''

# 根据项目id获取该项目下所有Case数据
@case.route('api/case/allCase', methods=['POST'])
@auth.login_required
def allcall():
    log.debug('/api/case/allCase')
    param = json.loads(request.data)
    cid = param['cid']
    pageNum = param['pageNum']
    pageSize = param['pageSize']

    if cid and pageNum and pageSize != None:
        data = cases.caseall_query(cid, pageNum, pageSize)
        log.info('根据cid【%s】获取的用例数据【%s】' % (cid, data))
        return {
            'code': '200',
            'data': data,
            'message': '成功'
        }
    else:
        return {
            'code': '403',
            'data': False,
            'message': '参数不完整'
        }


# 根据id查询Case信息
@case.route('api/case/infocase', methods=['GET'])
@auth.login_required
def infocase():
    log.debug('/api/case/infocase')
    id = request.args.get('id')
    value = cases.caseid_query(id)
    if value is not False:
        token_data = auth.decode(request.headers['token'])
        logs.logings(token_data[0], token_data[2], '根据id->' + str(id) + '查询用例数据')
        log.info('根据id【%s】获取的用例数据【%s】' % (id, value))
        return {
            'code': '200',
            'data': value,
            'message': '成功'
        }
    else:
        return {
            'code': '205',
            'data': value,
            'message': '未找到用例信息'
        }


# 获取用例查询类型数据
@case.route('api/case/SearchTypeList', methods=['GET'])
@auth.login_required
def casetypeList():
    log.debug('/api/case/SearchTypeList')
    data = cases.casetype_query()
    log.info('获取的用例类型数据【%s】' % data)
    return {
        'code': '200',
        'data': data,
        'message': '成功'
    }


# 根据用例类型和名称模糊查询数据
@case.route('api/case/search', methods=['POST'])
@auth.login_required
def vagueclase():
    log.debug('/api/case/search')
    param = json.loads(request.data)
    key = param['key']
    value = param['value']
    cid = param['cid']
    pageNum = param['pageNum']
    pageSize = param['pageSize']

    valuedata = cases.casetypes_query(cid, key, value, pageNum, pageSize)
    if cid and key and value and pageNum and pageSize != None:
        log.info('根据【%s】和【%s】查询出数据【%s】' % (key, value, valuedata))
        token_data = auth.decode(request.headers['token'])
        logs.logings(token_data[0], token_data[2], '根据cid->' + str(cid) + '和类型->' + key + '查询用例数据')
        return {
            'code': '200',
            'data': valuedata,
            'message': '成功'
        }
    else:
        return {
            'code': '403',
            'data': False,
            'message': '参数不完整'
        }


# 新增用例信息
@case.route('api/case/addclases', methods=['POST'])
@auth.login_required
def addclases():
    log.debug('/api/case/addclases')
    param = json.loads(request.data)
    moudle = param['moudle']
    title = param['title']
    url = param['url']
    methods = param['methods']
    headers = param['headers']
    leve = param['leve']
    case_param = param['case_param']
    judge = param['judge']
    asser = param['asser']      # int类型
    remark = param['remark']
    cid = param['cid']      # int类型

    if param is not None:
        values = cases.caseaddinformation(moudle, title, url, methods, headers, leve, case_param, judge, asser, remark, cid)
        log.info('新增cid【%s】项目下用例【%s】' % (cid, title))
        if values is None:
            token_data = auth.decode(request.headers['token'])
            logs.logings(token_data[0], token_data[2], '新增用例->'+"[" + title + "]" + '用例数据')
            return {
                'code': '200',
                'data': True,
                'message': '成功'
            }
        else:
            return {
                'code': '500',
                'data': values,
                'message': '数据库添加异常'
            }
    else:
        return {
                'code': '403',
                'data': False,
                'message': '参数不完整'
            }

# 根据id删除用例信息
@case.route('api/case/deletecase', methods=['DELETE'])
@auth.login_required
def removecase():
    log.debug('/api/case/deletecase')
    id = request.args.get('id')
    if id is not None:
        value = cases.casedel(id)
        if value is None:
            log.info('删除用例id【%s】的数据' % id)
            token_data = auth.decode(request.headers['token'])
            logs.logings(token_data[0], token_data[2], '删除id->' + str(id) + '的用例')
            return {
                'code': '200',
                'data': True,
                'message': '成功'
            }
        return {
                'code': '500',
                'data': value,
                'message': '数据库异常'
            }
    return {
        'code': '403',
        'data': False,
        'message': '参数不完整'
    }




# 根据id修改用例信息
@case.route('api/case/updatacase', methods=['PUT'])
@auth.login_required
def updatacase():
    log.debug('/api/case/updatacase')
    id = request.args.get('id') # 用列id
    param = json.loads(request.data)
    moudle = param['moudle']
    title = param['title']
    url = param['url']
    methods = param['methods']
    headers = param['headers']
    leve = param['leve']
    case_param = param['case_param']
    judge = param['judge']
    asser = param['asser']      # int类型
    remark = param['remark']
    cid = param['cid']  # int类型

    if id and param is not None:
        value = cases.caserevamp(moudle, title, url, methods, headers, leve, case_param, judge, asser, remark, cid, id)
        if value is None:
            log.info('修改cid【%s】项目下用例id【%s】的数据' % (cid, id))
            token_data = auth.decode(request.headers['token'])
            logs.logings(token_data[0], token_data[2], '修改项目id->' + "[" + id + "]的数据,名称改为->[" + title + "]")
            return {
                'code': '200',
                'data': True,
                'message': '成功'
            }
        return {
                'code': '500',
                'data': value,
                'message': '数据库异常'
            }
    return {
        'code': '403',
        'data': False,
        'message': '参数不完整'
    }


# 根据cid获取当日新增用例数和执行用例数
@case.route('api/case/number', methods=['POST'])
@auth.login_required
def newlynumber():
    log.debug('/api/case/number')
    param = json.loads(request.data)
    cid = param['cid']
    value = cases.case_todayquery(cid)
    log.info('根据项目id【%s】获取今日数据' % cid)
    if param is not None:
        return {
            'code': '200',
            'data': value,
            'message': '成功'
        }
    return {
        'code': '403',
        'data': False,
        'message': '参数不完整'
    }


