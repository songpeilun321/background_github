#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/22 15:54
# @Name    : peilun
# @File    : acquire_config.py
# @Software: PyCharm
# 获取config配置文件路径
import os
import yaml

path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
conpath = os.path.join(path, 'config') + '/config.yaml'

with open(conpath, 'r', encoding='utf-8')as f:
    data = yaml.load(f.read(), Loader=yaml.FullLoader)
    # data = yaml.load(f.read())


class getfunction():
    def __init__(self):
        self.env = data['env']
        self.host = data[self.env + '_' + 'host']
        self.port = data[self.env + '_' + 'port']
        self.user = data[self.env + '_' + 'user']
        self.passwd = data[self.env + '_' + 'passwd']
        self.library = data[self.env + '_' + 'library']
        self.debug = data[self.env + '_' + 'debug']
        self.host_ip = data[self.env + '_' + 'host_ip']
        self.host_port = data[self.env + '_' + 'host_port']
        self.jenk_host = data[self.env + '_' + 'jenk_host']
        self.jenk_name = data[self.env + '_' + 'jenk_name']
        self.jenk_pass = data[self.env + '_' + 'jenk_pass']
        self.redis_host = data[self.env + '_' + 'redis_host']
        self.redis_port = data[self.env + '_' + 'redis_port']
        self.redis_db = data[self.env + '_' + 'redis_db']
        self.redis_pwd = data[self.env + '_' + 'redis_pwd']


con = getfunction()