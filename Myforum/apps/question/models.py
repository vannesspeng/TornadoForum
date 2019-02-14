#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:pyy
# datetime:2018/12/29 10:33
from peewee import ForeignKeyField, CharField, TextField, IntegerField, JOIN

from Myforum.Forum.models import BaseModel
from Myforum.apps.users.models import User


class Question(BaseModel):
    user = ForeignKeyField(User, verbose_name="用户")
    category = CharField(max_length=200, verbose_name="分类", null=True)
    title = CharField(max_length=200, verbose_name="标题", null=True)
    content = TextField(verbose_name="内容")
    image = CharField(default=200, verbose_name="图片")
    answer_nums = IntegerField(default=0, verbose_name="回答数")

    @classmethod
    def extend(cls):
        return cls.select(cls, User.id, User.nick_name).join(User)

class Answer(BaseModel):
    # 回答和回复
    user = ForeignKeyField(User, verbose_name="用户", related_name="answer_author"),
    question = ForeignKeyField(Question, verbose_name="问题")
    parent_answer = ForeignKeyField('self', null=True, verbose_name="回答", related_name="answer_parent")
    question_user = ForeignKeyField(User, verbose_name="用户", related_name="question_user", null=True)
    content = CharField(max_length=1000, verbose_name="内容")
    reply_nums = IntegerField(default=0, verbose_name="回复数")

    @classmethod
    def extend(cls):
        #1. 多表join
        #2. 多字段映射同一个model
        answer_author = User.alias()
        question_user = User.alias()
        return cls.select(cls, Question, answer_author.id, answer_author.nick_name, question_user.id, question_user.nick_name).join(
            Question, join_type=JOIN.LEFT_OUTER, on=cls.question).switch(cls).join(answer_author, join_type=JOIN.LEFT_OUTER, on=cls.user).switch(cls).join(
            question_user, join_type=JOIN.LEFT_OUTER, on=cls.answer_user
        )