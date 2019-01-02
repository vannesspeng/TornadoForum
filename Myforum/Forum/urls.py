#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:pyy
# datetime:2018/12/28 15:18

from tornado.web import url, StaticFileHandler

import Myforum.apps.users.urls as user_urls
import Myforum.apps.community.urls as community_urls
import Myforum.apps.question.urls as question_urls
from Myforum.Forum.handlers import IndexHandler
from Myforum.Forum.settings import settings

urlpattern = [
    (url("/", IndexHandler, name="index")),
    (url("/media/(.*)", StaticFileHandler, {"path": settings["MEDIA_ROOT"]}))
]

urlpattern += user_urls.urlpattern
urlpattern += community_urls.urlpattern
urlpattern += question_urls.urlpattern

