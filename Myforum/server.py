#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:pyy
# datetime:2018/12/29 10:24

import tornado
from peewee_async import Manager
from tornado import web

from Myforum.Forum.settings import settings, database
from Myforum.Forum.urls import urlpattern

if __name__ == "__main__":
    # 集成json到wtforms中
    import wtforms_json
    wtforms_json.init()

    # 创建application对象，传入urlpattern、debug、settings等基础参数
    app = web.Application(urlpattern, debug=True, **settings)
    app.listen(8888)

    # 将数据库管理对象Manager，放入到application对象中
    objects = Manager(database=database)
    database.set_allow_sync(False)
    app.objects = objects


    tornado.ioloop.IOLoop.current().start()
