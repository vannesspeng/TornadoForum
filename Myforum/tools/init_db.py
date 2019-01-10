#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:pyy
# datetime:2019/1/4 11:06
from peewee import MySQLDatabase

from Myforum.apps.users.models import User
from Myforum.apps.community.models import CommunityGroup, CommunityGroupMember

database = MySQLDatabase(
    'myforum', host="127.0.0.1", port=3306, user="root", password="root"
)

def init():
    #生成表
    #database.create_tables([User])
    database.create_tables(([CommunityGroup, CommunityGroupMember]))


if __name__ == "__main__":
    init()
