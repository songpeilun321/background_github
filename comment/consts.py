#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 3:11 下午
# @Name    : peilun
# @File    : consts.py
# @Software: PyCharm
import json

'''
存放接口返回所需信息，将一些接口信息返回保存内存中，用例执行完成释放。
与PublicResource不同，这里信息都是接口即时获取，PublicResource是读取配置文件固定信息
'''


# 用户信息返回
class Info(object):
    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __getattr__(self, item):
        return self.__dict__[item]

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __getitem__(self, item):
        return self.__getattr__(item)

    def __str__(self):
        return json.dumps(self.__dict__)


info = Info()
