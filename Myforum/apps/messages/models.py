#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:pyy
# datetime:2018/12/29 10:33
from peewee import ForeignKeyField, CharField, IntegerField

from Myforum.Forum.models import BaseModel
from Myforum.apps.users.models import User

MESSAGES_TYPES = (
    (1, "评论"),
    (2, "帖子回复"),
    (3, "点赞"),
    (4, "回答"),
    (5, "回答的答复"),
)

class Message(BaseModel):
    sender = ForeignKeyField(User, verbose_name="发送者", related_name="message_sender")
    receiver = ForeignKeyField(User, verbose_name="接受者", related_name="message_receiver")
    message_type = IntegerField(choices=MESSAGES_TYPES, verbose_name="类别")
    message = CharField(max_length=500, verbose_name="内容", null=True)
    parent_content = CharField(max_length=500, verbose_name="标题", null=True)

