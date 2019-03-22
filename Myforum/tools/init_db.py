#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:pyy
# datetime:2019/1/4 11:06
from peewee import MySQLDatabase

from Myforum.apps.community.models import CommunityGroup, CommunityGroupMember, Post, PostComment, CommentLike
from Myforum.apps.messages.models import Message
from Myforum.apps.question.models import Question, Answer

database = MySQLDatabase(
    'myforum', host="127.0.0.1", port=3306, user="root", password="root"
)

def init():
    #生成表
    #database.create_tables([User])
    #database.create_tables(([CommunityGroup, CommunityGroupMember]))
    #database.create_tables(([ Post, PostComment, CommentLike]))
    #database.create_tables(([Question, Answemessages_setr]))
    database.create_tables(([Message]))


if __name__ == "__main__":
    init()
