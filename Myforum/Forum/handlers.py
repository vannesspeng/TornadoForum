#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:pyy
# datetime:2018/12/28 15:17
import redis
from tornado.web import RequestHandler


class IndexHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.write("Hello Tornado!!!")

class BaseHandler(RequestHandler):

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, DELETE, PUT, PATCH, OPTIONS')
        self.set_header('Access-Control-Allow-Headers',
                        'Content-Type, tsessionid, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')

    def options(self, *args, **kwargs):
        pass

class RedisHandler(BaseHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__( application, request, **kwargs)
        self.redis_conn = redis.StrictRedis(**self.settings["redis"])
