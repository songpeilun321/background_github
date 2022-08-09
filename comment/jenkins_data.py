#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/7 11:17
# @Name    : peilun
# @File    : jenkins_data.py
# @Software: PyCharm
from comment.acquire_config import con
from comment.log import log
import jenkins
import time


class Jendata():
    def __init__(self):
        self.errorMsg = ""
        self.tile = time.strftime("%Y-%m-%d %H:%M:%S")
        self.server = jenkins.Jenkins(con.jenk_host, username=con.jenk_name, password=str(con.jenk_pass))


    def get_status(self, name):
        '''
        获取job当前运行的状态
        :return:
        '''
        try:
            job_name = 'job/' + name + '/'  # job名称
            job_last_number = self.server.get_info(job_name)['lastBuild']['number']
            build_state = self.server.get_build_info(name, job_last_number)['result']
            return build_state
        except Exception as e:
            self.errorMsg = str(e)
            log.error("项目不存在 %s" % e)
            return False


    def structure(self, name):
        '''
        执行job 运行
        :param name:
        :return:
        '''

        try:
            data = self.server.build_job(name)
            job_name = 'job/' + name + '/'  # job名称
            job_last_number = self.server.get_info(job_name)['lastBuild']['number']
            time.sleep(3)
            build_state = self.server.get_build_info(name, job_last_number)['result']
            if data is not None:
                return build_state
        except Exception as e:
            self.errorMsg = str(e)
            log.error("项目不存在 %s" % e)
            return False

    def lastdata(self, name):
        '''
        :return: 获取最近一次构建记录url地址
        '''
        try:
            job_name = 'job/'+name+'/'  # job名称
            job_url = con.jenk_host + job_name  # job的url地址
            job_last_number = self.server.get_info(job_name)['lastBuild']['number']
            report_url = job_url + str(job_last_number) + '/allure'  # 报告地址
            return report_url
        except Exception as e:
            self.errorMsg = str(e)
            log.error("jenkins连接异常 %s" % e)


    def jenlogs(self, name):
        # 输出构建日志
        try:
            job_name = 'job/'+name+'/'  # job名称
            job_last_number = self.server.get_info(job_name)['lastBuild']['number']
            data = self.server.get_build_console_output(name, job_last_number)
            if data is not None:
                value = {
                    'code': '200',
                    'data': data,
                    'message': '成功'

                    }
                return value
        except Exception as e:
            self.errorMsg = str(e)
            log.error("日志不存在 %s" % e)
            return False



jen = Jendata()