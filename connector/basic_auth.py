#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/1 15:00
# @Name    : peilun
# @File    : case_auth.py
# @Software: PyCharm

from flask import request, Blueprint, session
from comment.flask_apiauth import auth
from comment.db_manipulation import base, logs
from comment.log import log
from utils.redis_utils import *
import json

user = Blueprint('user', __name__)

'''
    用户接口
'''

# 用户登录
@user.route('api/user/login', methods=['POST'])
def get_auth():
    log.debug('/api/user/login')
    param = json.loads(request.data)
    username = param['username']
    password = param['password']
    if username and password:
        data = base.userlogin_query(password, username)
        if data is not None:
            if data[4] == 0:
                token = auth.get_token(id=data[0], username=data[1], password=data[2], designation=data[3])
            else:
                logs.logings(data[0], data[3], '已被禁用')
                log.info('用户: 【%s】 已经被禁用' % (data[3]))
                return {
                    'code': '403',
                    'data': False,
                    'message': '用户已被禁用,请联系管理员!!!'
                }
            logs.logings(data[0], data[3], '登录成功')
            log.info('用户: 【%s】 登录成功! Token:【%s】' % (data[3], token))
            # 将登录成功后的token写入redis缓存
            userkey = str(data[0])+'_USER_'+data[1].upper()
            set_with_expireTime(userkey, token, 6000)
            return {
                'code': '200',
                'data': {
                    'token': token,
                    'userinfo': {'user_id': data[0],
                                 'user': data[1],
                                 'name': data[3],
                                 'state': data[4]
                                 }
                },
                'message': '登录成功'
            }
        else:
            return {
                'code': '400',
                'data': False,
                'message': '登录失败，用户名或密码有误'
            }
    else:
        return {
                'code': '403',
                'data': False,
                'message': '参数不完整'
            }

# 获取所有用户信息
@user.route('api/user/alluser', methods=['GET'])
@auth.login_required
def alluser():
    log.debug('/api/user/alluser')
    datauser = base.userown_query()
    token = request.args.get('token')
    if token != 'NULL':
        log.info('所有用户信息: 【%s】' % datauser)
        return {
            'code': '200',
            'data': datauser,
            'message': '成功'
        }
    return {
        'code': '403',
        'data': False,
        'message': 'token已失效'
    }


# 根据id查询用户信息
@user.route('api/user/information', methods=['GET'])
@auth.login_required
def information():
    log.debug('/api/user/information')
    id = request.args.get('id')
    value = base.userid_query(id)
    token_data = auth.decode(request.headers['token'])
    logs.logings(token_data[0], token_data[2], '根据id->'+str(id)+'查询用户数据')
    log.info('根据用户id【%s】 查询出信息 【%s】' % (id, value))
    if value is not False:
        return {
            'code': '200',
            'data': value,
            'message': '成功'
        }
    else:
        return {
            'code': '205',
            'data': value,
            'message': '未找到用户信息'

        }

# 根据名称模糊查询用户信息
@user.route('api/user/value', methods=['GET'])
@auth.login_required
def vertical():
    log.debug('/api/user/value')
    username = request.args.get('username')
    valuedata = base.username_query(username)
    token_data = auth.decode(request.headers['token'])
    logs.logings(token_data[0], token_data[2], '根据用户名称'+"["+username+"]"+'查询用户数据')
    log.info('根据用户name【%s】 查询出信息 【%s】' % (username, valuedata))
    if valuedata is not False:
        return {
            'code': '200',
            'data': valuedata,
            'message': '成功'
        }
    else:
        return {
            'code': '205',
            'data': valuedata,
            'message': '未找到用户信息'

        }


# 新增用户信息
@user.route('api/user/addusers', methods=['POST'])
@auth.login_required
def addusers():
    log.debug('/api/user/addusers')
    param = json.loads(request.data)
    user = param['user']
    word = param['pass']
    name = param['designation']
    sex = param['sex']
    job = param['job']
    disb = param['is_disable']
    log.info('新增用户【%s】' % name)
    if param is not None:
        values = base.useraddition(user, word, name, sex, job, disb)
        if values is None:
            log.info('新增用户【%s】信息【%s】' %(name, values))
            token_data = auth.decode(request.headers['token'])
            logs.logings(token_data[0], token_data[2], '新增名称' + "[" + name + "]" + '用户')
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

# 根据id修改用户信息 不支持修改密码
@user.route('api/user/updatauser', methods=['PUT'])
@auth.login_required
def updatauser():
    log.debug('/api/user/updatauser')
    id = request.args.get('id') # 用户id
    param = json.loads(request.data)
    user = param['user']
    name = param['designation']
    sex = param['sex']  # int类型
    jpb = param['job']
    is_disable = param['is_disable'] # 用户状态
    if id and param is not None:
        value = base.useralter(id, user, name, sex, jpb, is_disable)
        if value is None:
            log.info('根据id【%s】修改【%s】信息【%s】' % (id, name, value))
            token_data = auth.decode(request.headers['token'])
            logs.logings(token_data[0], token_data[2], '修改项目cid->' + "[" + str(id) + "]的数据,名称改为->[" + name + "]")

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

# 根据id修改状态信息
@user.route('api/user/updatauserid', methods=['PUT'])
@auth.login_required
def updatauserid():
    log.debug('/api/user/updatauserid')
    id = request.args.get('id') # 用户id
    param = json.loads(request.data)
    is_disable = param['is_disable'] # 用户状态
    if id and param is not None:
        value = base.useralterstatus(id, is_disable)
        if value is None:
            log.info('根据id【%s】修改状态为【%s】信息【%s】' % (id, is_disable, value))
            token_data = auth.decode(request.headers['token'])
            logs.logings(token_data[0], token_data[2], 'id为' + str(id) + '的用户,状态修改-> %s' % is_disable)
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

# 根据id删除用户信息
@user.route('api/user/deleteuser', methods=['DELETE'])
@auth.login_required
def removeuserid():
    log.debug('api/user/deleteuser')
    id = request.args.get('id')
    log.info('删除用户id【%s】的信息' % id)
    if id is not None:
        value = base.useralterdel(id)
        if value is None:
            token_data = auth.decode(request.headers['token'])
            logs.logings(token_data[0], token_data[2], '删除id->' + str(id) + '的用户数据')
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


# 退出登录
@user.route('api/user/logout', methods=['GET'])
@auth.login_required
def logout():
    token_data = auth.decode(request.headers['token'])
    value = str(token_data[0])+'_USER_'+token_data[1].upper()
    remove(value)
    logs.logings(token_data[0], token_data[2], '已安全退出')
    return {
        'code': '200',
        'data': {},
        'message': '退出成功'
  }