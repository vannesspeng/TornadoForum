#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:pyy
# datetime:2019/2/14 10:13
from wtforms import StringField, TextAreaField, IntegerField
from wtforms.validators import AnyOf, DataRequired, Length
from wtforms_tornado import Form


class QuestionForm(Form):
    category = StringField("类别", validators=[AnyOf(values=["技术问答", "技术分享", "活动建议"])])
    title = StringField("标题", validators=[DataRequired(message="请输入标题")])
    content = TextAreaField("简介", validators=[DataRequired(message="请输入内容")])

class AnswerForm(Form):
    content = StringField("内容", validators=[DataRequired("请输入评论内容"),
                                            Length(min=5, message="内容不能少于5个字符")])

class AnswerReplyForm(Form):
    replyed_user = IntegerField("回复用户", validators=[DataRequired("请输入回复用户")])
    content = StringField("内容", validators=[DataRequired("请输入评论内容"),
                                            Length(min=3, message="内容不能少于3个字符")])