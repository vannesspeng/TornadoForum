#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:pyy
# datetime:2019/1/9 15:20
from wtforms import StringField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, AnyOf, Length
from wtforms_tornado import Form


class CommunityGroupForm(Form):
    name = StringField("名称", validators=[DataRequired("请输入小组名称")])
    category = StringField("类别", validators=[AnyOf(values=["Python Web开发", "网络爬虫", "云计算与数据分析", "人工智能"])])
    desc = TextAreaField("简介", validators=[DataRequired(message="请输入简介")])
    notice = TextAreaField("公告", validators=[DataRequired(message="请输入公告")])


class GroupApplyForm(Form):
    apply_reason = StringField("申请理由", validators=[DataRequired("请输入申请理由")])


class PostForm(Form):
    title = StringField("标题", validators=[DataRequired("请输入标题")])
    content = StringField("内容", validators=[DataRequired("请输入内容")])


class PostComentForm(Form):
    content = StringField("内容", validators=[DataRequired("请输入评论内容"), Length(min=5, message="评论内容不能少于5个字")])

class CommentReplyForm(Form):
    replyed_user = IntegerField("回复用户", validators=[DataRequired("请输入回复用户")])
    content = StringField("内容", validators=[DataRequired("请输入评论内容"),
                                            Length(min=5, message="内容不能少于5个字符")])