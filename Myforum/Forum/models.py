#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:pyy
# datetime:2018/12/28 15:18
from datetime import datetime
from Myforum.Forum.settings import database
from peewee import Model, DateTimeField


class BaseModel(Model):
    add_time = DateTimeField(default=datetime.now, verbose_name="添加时间")
    class Meta:
        database = database