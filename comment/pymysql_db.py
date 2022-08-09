#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/20 17:27
# @Name    : peilun
# @File    : pymysql_db.py
# @Software: PyCharm

import pymysql
from queue import Queue
from comment.log import log

class ConnectionPool(object):
    def __init__(self, **kwargs):
        self.size = kwargs.get('size', 100)
        self.kwargs = kwargs
        self.conn_queue = Queue(maxsize=self.size)

        for i in range(self.size):
            self.conn_queue.put(self._create_new_conn())

    def _create_new_conn(self):
        conn = pymysql.connect(host=self.kwargs.get('host'),
                               user=self.kwargs.get('user'),
                               db=self.kwargs.get('dbname'),
                               passwd=self.kwargs.get('password'),
                               port=self.kwargs.get('port'),
                               connect_timeout=5)
        conn.autocommit(1)
        return conn

    def _put_conn(self, conn):
        self.conn_queue.put(conn)

    def _get_conn(self):
        conn = self.conn_queue.get()

        if conn is None:
            self._create_new_conn()
        return conn

    # 执行sql
    def exec_sql(self, sql):
        conn = self._get_conn()
        # conn.autocommit(1)
        try:
            cur = conn.cursor()
            cur.execute(sql)
            return cur.fetchall()
        except pymysql.ProgrammingError as e:
            log.error('execute sql {{0}} error {1}'.format(sql, e))
            raise e
        except pymysql.OperationalError as e:
            conn = self._create_new_conn()
            raise e
        finally:
            self._put_conn(conn)

    def __del__(self):
        try:
            while True:
                conn = self.conn_queue.get_nowait()
                if conn:
                    conn.close()
        except Exception as e:
            pass
