#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:pyy
# datetime:2018/12/29 10:33
import json
from random import choices

from tornado.web import RequestHandler

from Myforum.Forum.handlers import RedisHandler
from Myforum.apps.users.forms import SmsCodeForm, RegisterForm
from Myforum.apps.users.models import User
from Myforum.apps.utils.AsyncYunPian import AsyncYunPian

class RegisterHandler(RedisHandler):
    async def post(self, *args, **kwargs):
        # 声明返回的数据字典
        re_data = {}
        # 获取post请求参数,此时的params为str
        param = self.request.body.decode("utf8")
        # 将params原始json数据转换为字典
        param = json.loads(param)
        register_form = RegisterForm.from_json(param)
        if register_form.validate():
            mobile = register_form.mobile.data
            code = register_form.code.data
            password = register_form.password.data

            # 在redis中查询验证码，来确定上传的验证码是否正确
            redis_key = "{}-{}".format(mobile, code)
            if not self.redis_conn.get(redis_key):
                # 说明验证码非法
                self.set_status(400)
                re_data['code'] = "验证码失效或者错误"
            else:
                # 验证正确，那么就需要验证用户是否存在
                try:
                    existed_users = await self.application.objects.get(User, mobile=mobile)
                    self.set_status(400)
                    re_data["mobile"] = "用户已经存在"
                except User.DoesNotExist as e:
                    user = await self.application.objects.create(User, mobile=mobile, password=password)
                    re_data['id'] = user.id
        else:
            self.set_status(400)
            for field in register_form.errors:
                re_data[field] = register_form.errors[field][0]
        self.finish(re_data)




class SmsHandler(RedisHandler):
    def general_code(self):
        """
        随机生成四位数的验证码
        :return:
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choices(seeds)[0])
        return "".join(str(x) for x in random_str)


    async def post(self, *args, **kwargs):
        re_data = {}
        # 获取post的请求参数
        param = self.request.body.decode("utf-8")
        param = json.loads(param)
        sms_form = SmsCodeForm.from_json(param)
        if sms_form.validate():
            # 使用云片网api发送短信到指定的手机号码上
            # 发送单条短信
            # 这里使用tornado框架中的httpclient来发送网络请求
            mobile = sms_form.mobile.data
            code = self.general_code()
            yu_pian = AsyncYunPian("37a35942325be7af542ca05b22aa16ab")
            re_json = await yu_pian.send_single_sms(code, mobile)
            if re_json["code"] != 0:
                self.set_status(400)
                re_data["mobile"] = re_json["msg"]
            else:
                # 说明请求成功，将验证码写入redis数据库
                self.redis_conn.set("{}-{}".format(mobile, code), 1, 30*60)
                re_data["success"] = re_json["msg"]
        else:
            self.set_status(400)
            for field in sms_form.errors:
                re_data[field] = sms_form.errors[field][0]
        self.finish(re_data)
