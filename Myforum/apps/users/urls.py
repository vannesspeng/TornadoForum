#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:pyy
# datetime:2018/12/29 10:34
from tornado.web import url

from Myforum.apps.users.handlers import SmsHandler, RegisterHandler, LoginHandler

urlpattern = (
    url("/code/", SmsHandler),
    url("/register/", RegisterHandler),
    url("/login/", LoginHandler)
)