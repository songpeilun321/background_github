#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/1 17:57
# @Name    : peilun
# @File    : run.py
# @Software: PyCharm
from comment.acquire_config import con
from flask import Flask
from connector.basic_auth import user
from connector.case_auth import case
from connector.fly_book import fb
from connector.jenk_auth import jenk
from connector.logs_auth import log

app = Flask(__name__)
app.register_blueprint(user, url_prefix="/")
app.register_blueprint(case, url_prefix="/")
app.register_blueprint(jenk, url_prefix="/")
app.register_blueprint(log, url_prefix="/")
# app.register_blueprint(configuration, url_prefix="/")
app.register_blueprint(fb, url_prefix="/api/fb")
app.secret_key = 'guest secret key'

if __name__ == '__main__':
    app.run(debug=con.debug, host=con.host_ip, port=con.host_port)
