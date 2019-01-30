#!/usr/bin/env python
# encoding: utf-8
from .handlers import *
from tornado.web import url

urlpattern = (
    url(r'/upload/', UploadHandler),
    url(r'/ueditor', UeditorHandler),
    url(r'/upload/(.*)', StaticFileHandler, {'path': 'upload'}),
)
