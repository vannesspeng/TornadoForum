#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:pyy
# datetime:2018/12/29 10:24

import tornado
from tornado import web

from Myforum.Forum.settings import settings
from Myforum.Forum.urls import urlpattern

if __name__ == "__main__":
    # 集成json到wtforms中
    import wtforms_json
    wtforms_json.init()

    # 创建application对象，传入urlpattern、debug、settings等基础参数
    app = web.Application(urlpattern, debug=True, **settings)
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
