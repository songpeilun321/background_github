#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/26 10:52
# @Name    : peilun
# @File    : configuration_auth.py
# @Software: PyCharm
from flask import request, Blueprint
from comment.flask_apiauth import auth
from comment.db_manipulation import logs
import json
'''
    系统配置相关接口
'''
configuration = Blueprint('configuration', __name__)

# 上传图片格式信息
FORMAT = ['png', 'jpg', 'jpeg']

#