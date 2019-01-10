#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:pyy
# datetime:2019/1/9 15:20
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, AnyOf
from wtforms_tornado import Form


class CommunityGroupForm(Form):
    name = StringField("名称", validators=[DataRequired("请输入小组名称")])
    category = StringField("类别", validators=[AnyOf(values=["教育同盟", "同城交易", "程序设计", "生活兴趣"])])
    desc = TextAreaField("简介", validators=[DataRequired(message="请输入简介")])
    notice = TextAreaField("简介", validators=[DataRequired(message="请输入公告")])
