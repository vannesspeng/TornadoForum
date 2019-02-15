#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:pyy
# datetime:2018/12/29 10:34
from tornado.web import url

from Myforum.apps.question.handlers import QuestionHandler, QuestionDetailHandler, AnswerHanlder, AnswerReplyHandler

urlpattern = (
    url("/questions/", QuestionHandler),
    url("/questions/([0-9]+)/", QuestionDetailHandler),

    #问题回答
    url("/questions/([0-9]+)/answers/", AnswerHanlder),
    url("/answers/([0-9]+)/replys/", AnswerReplyHandler),
)