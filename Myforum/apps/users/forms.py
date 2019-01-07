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
            DataRequired(message="请输入手机号码"),
            Regexp(MOBILE_REGEX, message="请输入合法的手机号码")
        ]
    )


class RegisterForm(Form):
    mobile = StringField("手机号码", validators=[
        DataRequired(message="请输入手机号码"),
        Regexp(MOBILE_REGEX, message="请输入合法的手机号码")
    ])
    code = StringField("验证码", validators=[DataRequired(message="请输入验证码")])
    password = StringField("密码", validators=[DataRequired(message="请输入验证码")])