#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/8 15:46
# @Name    : peilun
# @File    : test.py
# @Software: PyCharm
from datetime import datetime
from comment.db_manipulation import base
from werkzeug.security import generate_password_hash, check_password_hash
# 明文密码
# password = "admin"
# 生成加密哈希值
# data = base.username_check("zhansan")
# for i in range(len(data)):
#     print(data[i][1])
#     p_hash = check_password_hash(data[i][1], '123456')
#     if p_hash is not 'True':
#         print(p_hash)
        # break



# # 验证密码
# ret = check_password_hash(p_hash, password)
# print(ret)
#
# ret = check_password_hash(p_hash, "afdasfsda")
# print(ret)

# dd = "Fri Nov 09 2018 14:41:35 GMT+0800 (CST)"
#
# GMT_FORMAT = '%a %b %d %Y %H:%M:%S GMT+0800 (CST)'
#
# print(datetime.strptime(dd, GMT_FORMAT))


a = 111
print('nihao', a)


def sum(a, b, c):
    '''
    :param a: 毛重
    :param b: 皮重
    :param c: 单价
    :return: 总价钱
    '''
    return ((a*2)-(b*2))*c

def my_sum(*args):
    result = 0
    for x in args:
        result += x
    return result


print('第一车 单价1.44, 总价：', sum(2032, 790, 1.44))
print('第二车 价钱1.44, 总价：', sum(2312, 822, 1.44))
print('第三车 价钱1.44, 总价：', sum(2084, 790, 1.44))
print("------------------------")
print('第四车 价钱1.45, 总价：', sum(1468, 830, 1.45))
print('第五车 价钱1.45, 总价：', sum(1686, 788, 1.45))
print('第六车 价钱1.44, 总价：', sum(1672, 830, 1.45))
print('第七车 价钱1.45, 总价：', sum(1448, 834, 1.45))
print('第八车 价钱1.45, 总价：', sum(2282, 830, 1.45))
print('第九车 价钱1.45, 总价：', sum(1874, 700, 1.45))
print("------------------------")

print("总计：", my_sum(3576.96, 4291.2, 3726.72, 1850.2, 2604.2, 2441.7999999999997, 1780.6, 4210.8, 3404.6))