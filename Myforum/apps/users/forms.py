#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:pyy
# datetime:2019/1/2 15:32
from wtforms import StringField
from wtforms.validators import DataRequired, Regexp
from wtforms_tornado import Form

MOBILE_REGEX = "^1[358]\d{9}$|^1[48]7\d{8}$|^176\d{8}$"

class SmsCodeForm(Form):
    mobile = StringField("手机号码", validators=[
            DataRequired("请输入手机号码"),
            Regexp(MOBILE_REGEX, message="请输入合法的手机号码"),
        ],
    )