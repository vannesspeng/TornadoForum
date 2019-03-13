#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:pyy
# datetime:2019/1/2 15:32
from wtforms import StringField
from wtforms.validators import DataRequired, Regexp, Length
from wtforms_tornado import Form

MOBILE_REGEX = "^1[358]\d{9}$|^1[48]7\d{8}$|^176\d{8}$"


class LoginForm(Form):
    mobile = StringField("手机号码", validators=[
        DataRequired(message="请输入手机号码"),
        Regexp(MOBILE_REGEX, message="请输入合法的手机号码")
    ])
    password = StringField("密码", validators=[DataRequired(message="请输入密码")])


class SmsCodeForm(Form):
    mobile = StringField("手机号码", validators=[
        DataRequired(message="请输入手机号码"),
        Regexp(MOBILE_REGEX, message="请输入合法的手机号码")
    ])


class RegisterForm(Form):
    mobile = StringField("手机号码", validators=[
        DataRequired(message="请输入手机号码"),
        Regexp(MOBILE_REGEX, message="请输入合法的手机号码")
    ])
    code = StringField("验证码", validators=[DataRequired(message="请输入验证码")])
    password = StringField("密码", validators=[DataRequired(message="请输入密码")])

class ChangeInfoForm(Form):
    gender = StringField("性别", validators=[DataRequired(message="请选择性别")])
    nick_name = StringField("昵称", validators=[DataRequired(message="请输入昵称"), Length(max=20, message="个人简介不能少于超过20个字符")])
    address = StringField("地区", validators=[DataRequired(message="请输入地区")])
    desc = StringField('个人简介', validators=[Length(min=6, message="个人简介不能少于6个字符")])

class ChangePwdForm(Form):
    old_psw = StringField("旧密码", validators=[DataRequired(message="请选输入旧密码")])
    new_psw = StringField("新密码", validators=[DataRequired(message="请输入新密码")])
    confirm_psw = StringField("确认新密码", validators=[DataRequired(message="请确认新密码")])
