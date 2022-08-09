#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/12 10:21
# @Name    : peilun
# @File    : collocate.py
# @Software: PyCharm
from datetime import datetime

def datemoe(value):
    '''
    数据库获取时间转换
    :return:
    '''

    GMT_FORMAT = '%a %b %d %Y %H:%M:%S GMT+0800 (CST)'

    date = datetime.strptime(value, GMT_FORMAT)
    print(date)
    return date

dd = "Tue, 12 Apr 2022 09:38:08 GMT"