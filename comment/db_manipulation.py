#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/20 15:27
# @Name    : peilun
# @File    : db_manipulation.py
# @Software: PyCharm

from comment.pymysql_db import ConnectionPool
from comment.acquire_config import *
from comment.log import log
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

mysql_tool = ConnectionPool(
    host=con.host,
    user=con.user,
    password=con.passwd,
    dbname=con.library,
    port=con.port,
    size=5
)

# 用户相关查询
class Database:
    '''
    用户相关
    '''

    def userlogin_query(self, password, name):
        '''
        传入密码和账号登录判断用户是否存在
        :param password: 密码
        :param name: 名称
        :return: 用户登录成功
        '''
        try:
            sql_pu = ("SELECT password,username FROM Users")
            res = mysql_tool.exec_sql(sql_pu)
            for i in res:
                value = check_password_hash(i[0], password)
                if value is True and i[1] == name:
                    sql = "SELECT id, username, password, designation, is_disable FROM `storedcase`.`Users` WHERE `username` = " + "'" + name + "'"
                    log.info(sql)
                    res = mysql_tool.exec_sql(sql)
                    return res[0]
        except Exception as e:
            self.errorMsg = str(e)
            log.error("数据库连接异常", self.errorMsg)

    def userid_query(self, id):
        '''
        根据id查询用户信息
        :return:
        '''
        try:
            sql = " SELECT * FROM `Users` WHERE `id`= %s limit 1" % id
            log.info(sql)
            res = mysql_tool.exec_sql(sql)
            if res == ():
                return False
            a = {"user_id": res[0][0], "user": res[0][1], "name": res[0][3], "sex": res[0][4], "job": res[0][5], "disable": res[0][6]}
            return a
        except Exception as e:
            self.errorMsg = str(e)
            log.error("数据库连接异常", self.errorMsg)

    def username_query(self, name):
        '''
        根据name模糊查询用户信息
        :return:
        '''
        try:
            sql = " SELECT * FROM `Users` WHERE `designation` LIKE  concat('%','" + name + "','%')"
            log.info(sql)
            res = mysql_tool.exec_sql(sql)
            if res == ():
                return False
            list = []
            number = len(res)
            for index in range(number):
                a = {"user_id": res[index][0], "user": res[index][1], "name": res[index][3], "sex": res[index][4], "job": res[index][5], "disable": res[index][6]}
                list.append(a)
            return list
        except Exception as e:
            self.errorMsg = str(e)
            log.error("数据库连接异常", self.errorMsg)



    def userown_query(self):
        '''
        查询所有用户信息
        :return:
        '''
        try:
            sql = "SELECT * FROM `Users`"
            log.info(sql)
            res = mysql_tool.exec_sql(sql)
            result = []
            for index in range(len(res)):
                a = {"user_id": res[index][0], "user": res[index][1], "pass": res[index][2], "name": res[index][3], "sex": res[index][4], "job": res[index][5],
                 "disable": res[index][6]}
                result.append(a)
            return result
        except Exception as e:
            self.errorMsg = str(e)
            log.error("数据库连接异常", self.errorMsg)

    def useraddition(self, account, pasw, name, sex, jobs, stust):
        '''
        添加用户信息
        :return:
        '''
        try:
            pwd = generate_password_hash(str(pasw))
            sql = "INSERT INTO `Users`(`username`,`password`,`designation`,`sex`,`job`,`is_disable`) values (%s,%s,%s,%s,%s,%s)" % ("'"+account+"'", "'"+pwd+"'", "'"+name+"'", sex, "'"+jobs+"'", stust)
            log.info(sql)
            mysql_tool.exec_sql(sql)
        except Exception as e:
            self.errorMsg = str(e)
            log.error("数据库连接异常", self.errorMsg)


    def useralter(self, id, user, name, sex, job, is_disable):
        '''
        :return: 根据id修改用户信息
        '''
        try:
            sql = 'UPDATE `Users` set username = %s, designation = %s, sex = %s, job = %s, is_disable = %s where id = %s' % ("'"+user+"'", "'"+name+"'", sex, "'"+job+"'", is_disable, id)
            log.info(sql)
            mysql_tool.exec_sql(sql)
        except Exception as e:
            self.errorMsg = str(e)
            log.error("数据库连接异常", self.errorMsg)


    def useralterstatus(self, id, is_disable):
        '''
        :return: 根据id修改用户状态
        '''
        try:
            sql = "UPDATE `Users` set is_disable = %s where id = %s" % (is_disable, id)
            log.info(sql)
            mysql_tool.exec_sql(sql)
        except Exception as e:
            self.errorMsg = str(e)
            log.error("数据库连接异常", self.errorMsg)


    def useralterdel(self, id):
        '''
        :return: 根据id删除用户状态
        '''
        try:
            sql = "delete FROM `Users` WHERE id = %s" % id
            log.info(sql)
            mysql_tool.exec_sql(sql)
        except Exception as e:
            self.errorMsg = str(e)
            log.error("数据库连接异常", self.errorMsg)

class Datacase:
    '''
    用例相关
    '''
    def caseall_query(self, cid, pageNum, pageSize):
        '''
        :return: 根据项目cid查询所有用例信息
        '''
        try:
            sql = "SELECT * FROM `Case` WHERE `cid` = %s ORDER BY create_time DESC" % cid
            log.info(sql)
            data = mysql_tool.exec_sql(sql)
            total_size = len(data)
            start = (pageNum - 1) * pageSize
            end = start + pageSize
            list = []
            if total_size - end > 0:
                for index in range(start, end):
                    a = {"id": data[index][0], "name": data[index][1], "title": data[index][2], "url": data[index][3], "method": data[index][4],
                         "header": data[index][5], "leve": data[index][6], "param": data[index][7],
                         "judge": data[index][8], "assert": data[index][9], "remark": data[index][10], "cid": data[index][11], "time": data[index][12]}
                    list.append(a)
                page = {"pageNum": pageNum, "data": list, "total": total_size}
                return page
            else:
                for index in range(start, total_size):
                    a = {"id": data[index][0], "name": data[index][1], "title": data[index][2], "url": data[index][3], "method": data[index][4],
                         "header": data[index][5], "leve": data[index][6], "param": data[index][7],
                         "judge": data[index][8], "assert": data[index][9], "remark": data[index][10], "cid": data[index][11], "time": data[index][12]}
                    list.append(a)
                page = {"pageNum": pageNum, "data": list, "total": total_size}
                return page
        except Exception as e:
            self.errorMsg = str(e)
            log.error("数据库连接异常", self.errorMsg)

    def casetype_query(self):
        '''
        :return: 查询所有用例类型数据
        '''
        try:
            sql = "SELECT * FROM `CaseType`"
            log.info(sql)
            data = mysql_tool.exec_sql(sql)
            result = []
            for index in range(len(data)):
                a = {"id": data[index][0], "type": data[index][1], "title": data[index][2]}
                result.append(a)
            return result
        except Exception as e:
            self.errorMsg = str(e)
            log.error("数据库连接异常", self.errorMsg)


    def casetypes_query(self,cid, key, value, pageNum, pageSize):
        """
        :return: 根据选择用例类型获取数据
        """
        try:
            if key and value is not None:
                sql = "SELECT * FROM `Case` WHERE cid = " + str(cid) + " AND " + key + " LIKE  concat('%','" + value + "','%') ORDER BY create_time DESC"
                log.info(sql)
                data = mysql_tool.exec_sql(sql)
                total_size = len(data)
                start = (pageNum - 1) * pageSize
                end = start + pageSize
                list = []
                if total_size - end > 0:
                    for index in range(start, end):
                        a = {"id": data[index][0], "name": data[index][1], "title": data[index][2], "url": data[index][3],
                             "method": data[index][4],
                             "header": data[index][5], "leve": data[index][6], "param": data[index][7],
                             "judge": data[index][8], "assert": data[index][9], "remark": data[index][10],
                             "cid": data[index][11], "time": data[index][12]}
                        list.append(a)
                    page = {"pageNum": pageNum, "data": list, "total": total_size}
                    return page
                else:
                    for index in range(start, total_size):
                        a = {"id": data[index][0], "name": data[index][1], "title": data[index][2], "url": data[index][3],
                             "method": data[index][4],
                             "header": data[index][5], "leve": data[index][6], "param": data[index][7],
                             "judge": data[index][8], "assert": data[index][9], "remark": data[index][10],
                             "cid": data[index][11], "time": data[index][12]}
                        list.append(a)
                    page = {"pageNum": pageNum, "data": list, "total": total_size}
                    return page
            else:
                log.info("查询没有传入key/value")
                sql = "SELECT * FROM `Case` WHERE `cid` = %s ORDER BY create_time DESC" % cid
                log.info(sql)
                data = mysql_tool.exec_sql(sql)
                total_size = len(data)
                start = (pageNum - 1) * pageSize
                end = start + pageSize
                list = []
                if total_size - end > 0:
                    for index in range(start, end):
                        a = {"id": data[index][0], "name": data[index][1], "title": data[index][2],
                             "url": data[index][3], "method": data[index][4],
                             "header": data[index][5], "leve": data[index][6], "param": data[index][7],
                             "judge": data[index][8], "assert": data[index][9], "remark": data[index][10],
                             "cid": data[index][11], "time": data[index][12]}
                        list.append(a)
                    page = {"pageNum": pageNum, "data": list, "total": total_size}
                    return page
                else:
                    for index in range(start, total_size):
                        a = {"id": data[index][0], "name": data[index][1], "title": data[index][2],
                             "url": data[index][3], "method": data[index][4],
                             "header": data[index][5], "leve": data[index][6], "param": data[index][7],
                             "judge": data[index][8], "assert": data[index][9], "remark": data[index][10],
                             "cid": data[index][11], "time": data[index][12]}
                        list.append(a)
                    page = {"pageNum": pageNum, "data": list, "total": total_size}
                    return page
        except Exception as e:
            self.errorMsg = str(e)
            log.error("数据库连接异常", self.errorMsg)


    def caseid_query(self, id):
        '''
        :return:根据id查询用例Case数据
        '''
        try:
            sql = " SELECT * FROM `Case` WHERE `id` = %s limit 1" % id
            log.info(sql)
            data = mysql_tool.exec_sql(sql)
            if data == ():
                return False
            a = {"id": data[0][0], "name": data[0][1], "title": data[0][2], "url": data[0][3], "method": data[0][4],
                     "header": data[0][5], "leve": data[0][6], "param": data[0][7],
                     "judge": data[0][8], "assert": data[0][9], "remark": data[0][10], "cid": data[0][11], "time": data[0][12]}
            return a
        except Exception as e:
            self.errorMsg = str(e)
            log.error("数据库连接异常", self.errorMsg)


    def caseaddinformation(self, moudle, title, url, methods, headers, leve, Case_param, judge, asser, remark, cid):
        '''
        :return: 新增测试用例
        '''
        try:
            sql = "INSERT INTO `Case`(`moudle`,`title`,`url`,`methods`,`headers`,`leve`,`Case_param`,`judge`,`assert`,`remark`,`cid`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % ("'"+moudle+"'", "'"+title+"'", "'"+url+"'", "'"+methods+"'", "'"+headers+"'", "'"+leve+"'", "'"+Case_param+"'", "'"+judge+"'", asser, "'"+remark+"'", cid)
            log.info(sql)
            mysql_tool.exec_sql(sql)
        except Exception as e:
            self.errorMsg = str(e)
            log.error("数据库连接异常", self.errorMsg)


    def caserevamp(self, moudle, title, url, methods, headers,leve, Case_param, judge, asser,remark,cid, id):
        '''
        :return:根据id修改用例数据
        '''
        try:
            sql = "UPDATE `Case` set moudle = %s,title = %s, url = %s,methods = %s,headers = %s,leve = %s,Case_param = %s,judge = %s,assert = %s,remark = %s,cid = %s  where id = %s" % ("'"+moudle+"'", "'"+title+"'", "'"+url+"'", "'"+methods+"'", "'"+headers+"'", "'"+leve+"'", "'"+Case_param+"'", "'"+judge+"'", asser, "'"+remark+"'", cid, id)
            log.info(sql)
            mysql_tool.exec_sql(sql)
        except Exception as e:
            self.errorMsg = str(e)
            log.error("数据库连接异常", self.errorMsg)


    def casedel(self, id):
        '''
        :param id:
        :return: 删除用例信息
        '''
        try:
            sql = "delete FROM `Case` WHERE id = %s" % id
            log.info(sql)
            mysql_tool.exec_sql(sql)

        except Exception as e:
            self.errorMsg = str(e)
            log.error("数据库连接异常", self.errorMsg)


    def case_todayquery(self, cid):
        '''
        :return: 获取当日新增用例数和执行用例数
        '''
        start = datetime.now().strftime('%Y-%m-%d 00:00:00')
        end = datetime.now().strftime('%Y-%m-%d 23:59:59')
        try:
            if start and end is not None:
                casesql = "SELECT  COUNT(*) FROM `Case` WHERE `cid` = %s AND `create_time`>= %s AND `create_time` <= %s LIMIT 0,1000" % (cid, "'"+start+"'", "'"+end+"'")

                statsql = "SELECT  COUNT(*) FROM `Report_Data` WHERE `cid` = %s AND `create_time`>= %s AND `create_time` <= %s LIMIT 0,1000" % (cid, "'"+start+"'", "'"+end+"'")
                log.info(casesql)
                log.info(statsql)
                casedata = mysql_tool.exec_sql(casesql)
                statdata = mysql_tool.exec_sql(statsql)
                list = {"casesum": casedata[0][0], "operationsum": statdata[0][0]}
                return list
            return False
        except Exception as e:
            self.errorMsg = str(e)
            log.error("数据库连接异常", self.errorMsg)

class Datalogs:
    '''
    日志相关
    '''
    def logings(self, user_id, user_name, content):
        '''
        :return: 日志写入
        '''
        try:
            sql = "INSERT INTO `operation_log`(`operator_id`,`operator_name`,`operation_content`) value (%s ,%s ,%s)" % (user_id, "'"+user_name+"'", "'"+content+"'")
            log.info(sql)
            mysql_tool.exec_sql(sql)
        except Exception as e:
            self.errorMsg = str(e)
            log.error("数据库连接异常", self.errorMsg)


    def logsall_query(self, pageNum, pageSize):
        '''
        :return: 获取所有日志信息分页展示
        '''
        try:
            sql = "SELECT * FROM `operation_log` ORDER BY create_time DESC"
            log.info(sql)
            data = mysql_tool.exec_sql(sql)
            total_size = len(data)
            start = (pageNum - 1) * pageSize
            end = start + pageSize
            list = []
            if total_size - end > 0:
                for index in range(start, end):
                    a = {"operator_id": data[index][1], "operator_name": data[index][2], "operation_content": data[index][3], "create_time": data[index][4]}
                    list.append(a)
                page = {"pageNum": pageNum, "data": list, "total": total_size}
                print(page)
                return page
            else:
                for index in range(start, total_size):
                    a = {"operator_id": data[index][1], "operator_name": data[index][2], "operation_content": data[index][3], "create_time": data[index][4]}
                    list.append(a)
                page = {"pageNum": pageNum, "data": list, "total": total_size}
                return page
        except Exception as e:
            self.errorMsg = str(e)
            log.error("数据库连接异常", self.errorMsg)


    def logsname_query(self, name, pageNum, pageSize):
        '''
        :return: 根据用户名称查询日志信息
        '''
        try:
            sql = "SELECT * FROM `operation_log`WHERE `operator_name` = %s ORDER BY create_time DESC" % ("'"+name+"'")
            log.info(sql)
            data = mysql_tool.exec_sql(sql)
            total_size = len(data)
            start = (pageNum - 1) * pageSize
            end = start + pageSize
            list = []
            if total_size - end > 0:
                for index in range(start, end):
                    a = {"operator_name": data[index][2], "operation_content": data[index][3], "create_time": data[0][4]}
                    list.append(a)
                page = {"pageNum": pageNum, "data": list, "total": total_size}
                return page
            else:
                for index in range(start, total_size):
                    a = {"operator_name": data[index][2], "operation_content": data[index][3], "create_time": data[index][4]}
                    list.append(a)
                page = {"pageNum": pageNum, "data": list, "total": total_size}
                return page
        except Exception as e:
            self.errorMsg = str(e)
            log.error("数据库连接异常", self.errorMsg)

class Dataproject:
    """
    项目相关
    """
    def project_reportdata(self, cid, start, end):
        """
        :return: 根据项目id 和时间 获取运行结果数据
        """
        try:
            sql = "SELECT * FROM `Report_Data` WHERE `cid` = %s AND `create_time`>= %s AND `create_time` <= %s LIMIT 0,1000" % (cid, "'"+start+"'", "'"+end+"'")
            log.info(sql)
            data = mysql_tool.exec_sql(sql)
            result = []
            for index in range(len(data)):
                a = {"id": data[index][0], "sum": data[index][1], "passed": data[index][2], "failed": data[index][3], "broken": data[index][4], "skipped": data[index][5],
                 "cid": data[index][7], "time": data[index][8]}
                result.append(a)
            return result
        except Exception as e:
            self.errorMsg = str(e)
            log.error("数据库连接异常", self.errorMsg)


    def project_recently(self, cid):
        """
        :return: 根据项目id获取最近一条报告记录
        """
        try:
            sql = "SELECT * FROM Report_Data WHERE `cid` = %s ORDER BY create_time DESC LIMIT 1" % cid
            log.info(sql)
            data = mysql_tool.exec_sql(sql)
            result = []
            for index in range(len(data)):
                a = {"id": data[index][0], "passed": data[index][2], "failed": data[index][3], "broken": data[index][4], "skipped": data[index][5],
                 "cid": data[index][7], "time": data[index][8]}
                result.append(a)
            return result
        except Exception as e:
            self.errorMsg = str(e)
            log.error("数据库连接异常", self.errorMsg)


    def projectall_query(self):
        """
        :return: 获取项目全部数据
        """
        try:
            sql = "SELECT * FROM `Project`"
            log.info(sql)
            data = mysql_tool.exec_sql(sql)
            result = []
            for index in range(len(data)):
                a = {"cid": data[index][0], "proname": data[index][1], "jobname": data[index][2], "time": data[index][3]}
                result.append(a)
            return result
        except Exception as e:
            self.errorMsg = str(e)
            log.error("数据库连接异常", self.errorMsg)


    def projectname_query(self, jobname):
        '''
        :return: 根据输入的名称来获取项目名称
        '''
        try:
            sql = "SELECT jobnanme FROM `Project` WHERE `jobnanme`= %s" % ("'"+jobname+"'")
            log.info(sql)
            data = mysql_tool.exec_sql(sql)
            if data == ():
                return False
            return data[0][0]
        except Exception as e:
            self.errorMsg = str(e)
            log.error("数据库连接异常", self.errorMsg)


    def addproject(self, name, jobname):
        '''
        新增项目(先查询输入的name和数据库的name是否重复)
        :return:
        '''
        try:
            sql = "INSERT INTO `Project`(`name`,`jobnanme`) values (%s, %s)" % ("'"+name+"'", "'"+jobname+"'")
            log.info(sql)
            mysql_tool.exec_sql(sql)
        except Exception as e:
            self.errorMsg = str(e)
            log.error("数据库连接异常", self.errorMsg)


    def alterproject(self, cid, name, jobname):
        '''
        根据项目cid修改信息
        :return:
        '''
        try:
            sql = "UPDATE `Project` set name = %s,jobnanme = %s where cid = %s" % ("'"+name+"'", "'"+jobname+"'", cid)
            log.info(sql)
            mysql_tool.exec_sql(sql)
        except Exception as e:
            self.errorMsg = str(e)
            log.error("数据库连接异常", self.errorMsg)


    def delprojectcase(self, cid):
        '''
        查询项目下是否有用例
        :return:
        '''
        try:
            sql = "SELECT count(*) FROM `Case` WHERE `cid` = %s" % cid
            log.info(sql)
            data = mysql_tool.exec_sql(sql)
            return data[0][0]
        except Exception as e:
            self.errorMsg = str(e)
            log.error("数据库连接异常", self.errorMsg)

    def delproject(self, cid):
        '''
        根据项目cid删除数据（删除需要判断项目下是否有用例）
        :param cid:
        :return:
        '''
        try:
            sql = "SELECT * FROM `Case` WHERE `cid` = %s" % cid

            log.info(sql)
            data = mysql_tool.exec_sql(sql)
            if len(data) > 0:
                log.debug('项目cid【%s】下存在用例，无法删除！' % cid)
            else:
                delsql = "delete FROM `Project` WHERE cid = %s" % cid
                log.info(delsql)
                mysql_tool.exec_sql(delsql)
        except Exception as e:
            self.errorMsg = str(e)
            log.error("数据库连接异常", self.errorMsg)






base = Database()
cases = Datacase()
logs = Datalogs()
project = Dataproject()
