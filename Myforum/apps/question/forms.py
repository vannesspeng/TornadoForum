#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:pyy
# datetime:2019/2/14 10:13
from wtforms import StringField, TextAreaField
from wtforms.validators import AnyOf, DataRequired
from wtforms_tornado import Form


class QuestionForm(Form):
    category = StringField("类别", validators=[AnyOf(values=["技术问答", "技术分享", "活动建议"])])
    title = StringField("标题", validators=[DataRequired(message="请输入标题")])
    content = TextAreaField("简介", validators=[DataRequired(message="请输入内容")])