#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:pyy
# datetime:2018/12/29 10:33
import json
from random import choices

from tornado.web import RequestHandler

from Myforum.Forum.handlers import RedisHandler
from Myforum.apps.users.forms import SmsCodeForm
from Myforum.apps.utils.AsyncYunPian import AsyncYunPian


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
                self.redis_conn.set("{}-{}".format(mobile, code), 1, 10*60)
                re_data["success"] = re_json["msg"]
        else:
            self.set_status(400)
            for field in sms_form.errors:
                re_data[field] = sms_form.errors[field][0]
        return re_data
