#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:pyy
# datetime:2018/12/28 15:30
from tornado.web import url

from Myforum.apps.community.handlers import GroupHandler

urlpattern = (
    url("/groups/", GroupHandler),
)