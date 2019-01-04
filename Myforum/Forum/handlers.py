#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:pyy
# datetime:2018/12/28 15:17
import redis
from tornado.web import RequestHandler


class IndexHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.write("Hello Tornado!!!")

class RedisHandler(RequestHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__( application, request, **kwargs)
        self.redis_conn = redis.StrictRedis(**self.settings["redis"])
