#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:pyy
# datetime:2018/12/29 10:34
from tornado.web import url

from Myforum.apps.users.handlers import SmsHandler, RegisterHandler, LoginHandler, InfoHandler, HeadImageHandler, \
    PasswordHandler, UserGroupHanlder, UserQuestionHanlder, UserAnswerHanlder

urlpattern = (
    url("/code/", SmsHandler),
    url("/register/", RegisterHandler),
    url("/login/", LoginHandler),
    url("/info/", InfoHandler),
    url("/headimages/", HeadImageHandler),
    url("/password/", PasswordHandler),
    url("/users/([0-9]+)/groups/", UserGroupHanlder),
    url("/users/([0-9]+)/questions/", UserQuestionHanlder),
    url("/users/([0-9]+)/answers/", UserAnswerHanlder)
)