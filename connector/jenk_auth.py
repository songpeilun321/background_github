#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/7 17:54
# @Name    : peilun
# @File    : jenk_auth.py
# @Software: PyCharm
from flask import request, Blueprint
from comment.flask_apiauth import auth
from comment.jenkins_data import jen
from comment.db_manipulation import project, logs
from comment.log import log
import json

'''
    jenkins/项目接口
'''
jenk = Blueprint('jenk', __name__)

# 获取最近一次构建记录
@jenk.route('api/jenkins/record', methods=['GET'])
@auth.login_required
def record():
    log.debug('/api/jenkins/record')
    jobnanme = request.args.get('jobnanme')
    if jobnanme is not None:
        data = jen.lastdata(jobnanme)
        log.info('查看项目名称【%s】下最近一次构建记录【%s】' % (jobnanme, data))
        token_data = auth.decode(request.headers['token'])
        logs.logings(token_data[0], token_data[2], "查看->" +"["+jobnanme+"]"+"最近一次构建记录")
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



# 根据输入的名称来判断项目是否存在，存在则执行
@jenk.route('api/jenkins/executejob', methods=['GET'])
@auth.login_required
def executejob():
    log.debug('/api/jenkins/executejob')
    name = request.args.get('jobnanme')
    jobdata = project.projectname_query(name)
    if name is not None:
        log.info('输入项目名称【%s】执行该【%s】项目下用例' % (name, jobdata))
        try:
            if name in jobdata:
                jobstate = jen.structure(jobdata)
                token_data = auth.decode(request.headers['token'])
                logs.logings(token_data[0], token_data[2], '执行->'+"["+jobdata+"]项目下用例")
                return {
                    'code': '200',
                    'data': jobstate,
                    'message': '请求已发送，请30s后刷新页面'
                }
        except Exception:
            return {
                'code': '403',
                'data': jobdata,
                'message': '项目不存在'
            }
    else:
        return {
            'code': '403',
            'data': False,
            'message': '参数不完整'
        }


# 根据项目id和时间段返回执行结果
@jenk.route('api/jenkins/result', methods=['POST'])
@auth.login_required
def jenresult():
    log.debug('/api/jenkins/result')
    param = json.loads(request.data)
    cid = param['cid']
    start = param['start']
    end = param['end']

    if param is not None:
        data = project.project_reportdata(cid, start, end)
        log.info('根据项目【%s】查询数据【%s】' % (cid, data))
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


# 根据项目id查找执行结果
@jenk.route('api/jenkins/resultcid', methods=['GET'])
@auth.login_required
def resultcid():
    log.debug('/api/jenkins/resultcid')
    cid = request.args.get('cid')

    if cid is not None:
        data = project.project_recently(cid)
        log.info('根据项目id【%s】查询数据【%s】' % (cid, data))
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


# 获取项目信息数据
@jenk.route('api/project/project', methods=['GET'])
@auth.login_required
def getProject():
    log.debug('/api/project/project')
    data = project.projectall_query()
    return {
        'code': '200',
        'data': data,
        'message': '成功'
        }


# 新增项目
@jenk.route('api/project/addproject', methods=['POST'])
@auth.login_required
def addProject():
    log.debug('/api/project/addproject')
    param = json.loads(request.data)
    name = param['name']
    jobname = param['jobname']
    jobdata = project.projectname_query(jobname)
    if name and jobname is not None:
        log.info('输入项目名称【%s】执行该【%s】项目下用例' % (name, jobdata))
        if jobname == jobdata:
            log.info('项目【%s】已存在!' % jobdata)
            return {
                'code': '200',
                'data': False,
                'message': '项目【%s】已存在' % jobdata
            }
        else:
            project.addproject(name, jobname)
            token_data = auth.decode(request.headers['token'])
            logs.logings(token_data[0], token_data[2], '新增项目【%s】' % jobname)
            return {
                'code': '200',
                'data': jobdata,
                'message': '成功'
            }
    else:
        return {
            'code': '403',
            'data': False,
            'message': '参数不完整'
        }



# 修改项目信息
@jenk.route('api/project/alterproject', methods=['POST'])
@auth.login_required
def alterProject():
    log.debug('/api/project/alterproject')
    param = json.loads(request.data)
    cid = param['cid']
    name = param['name']
    jobname = param['jobname']
    jobdata = project.projectname_query(jobname)
    if name and jobname and cid is not None:
        if jobname == jobdata:
            log.info('项目【%s】已存在!' % jobdata)
            return {
                'code': '200',
                'data': False,
                'message': '项目【%s】已存在' % jobdata
            }
        else:
            log.info('修改项目cid【%s】名称改为【%s】' % (cid, jobname))
            token_data = auth.decode(request.headers['token'])
            logs.logings(token_data[0], token_data[2], '修改项目cid->' + "[" + str(cid) + "]的数据,名称改为->[" + jobname + "]")
            project.alterproject(cid, name, jobname)
            return {
                'code': '200',
                'data': True,
                'message': '成功'
            }
    else:
        return {
            'code': '403',
            'data': False,
            'message': '参数不完整'
        }

# 删除项目信息
@jenk.route('api/project/delproject', methods=['DELETE'])
@auth.login_required
def delProject():
    log.debug('/api/project/delproject')
    cid = request.args.get('cid')
    if cid is not None:
        value = project.delprojectcase(cid)
        if value > 0:
            log.debug('项目cid【%s】下存在用例，无法删除！' % cid)
            return {
                'code': '403',
                'data': False,
                'message': '项目cid【%s】下存在用例，无法删除！' % cid
            }
        else:
            token_data = auth.decode(request.headers['token'])
            logs.logings(token_data[0], token_data[2], '删除cid->' + "[" + str(cid) + "]项目")
            project.delproject(cid)
            return {
                'code': '200',
                'data': True,
                'message': '成功'
            }
    else:
        return {
            'code': '403',
            'data': False,
            'message': '参数不完整'
        }