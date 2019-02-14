#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:pyy
# datetime:2018/12/28 15:30
from tornado.web import url

from Myforum.apps.community.handlers import GroupHandler, GroupMemberHandler, GroupDetailHanlder, PostHandler, \
    PostDetailHandler, PostCommentHanlder, CommentReplyHandler, CommentsLikeHanlder

urlpattern = (
    url("/groups/", GroupHandler),
    url("/groups/([0-9]+)/", GroupDetailHanlder),
    url("/groups/([0-9]+)/members/", GroupMemberHandler),
    url("/groups/([0-9]+)/posts/", PostHandler),
    url("/posts/([0-9]+)/", PostDetailHandler),
    url("/posts/([0-9]+)/comments/", PostCommentHanlder),
    url("/comments/([0-9]+)/replys/", CommentReplyHandler),
    url("/comments/([0-9]+)/likes/", CommentsLikeHanlder)
)