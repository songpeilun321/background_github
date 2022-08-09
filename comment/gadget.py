#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/19 18:00
# @Name    : peilun
# @File    : gadget.py
# @Software: PyCharm
from datetime import date

def todaystart():

    yesterday = (date.today().strftime("%Y-%m-%d"))
    return yesterday +" 00:00:00"


def todayend():

    yesterday = (date.today().strftime("%Y-%m-%d"))
    return yesterday +" 23:59:59"
