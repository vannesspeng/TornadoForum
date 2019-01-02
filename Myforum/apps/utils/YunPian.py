#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:pyy
# datetime:2019/1/2 9:26
import requests


class YunPian:
    def __init__(self, api_key):
        self.api_key = api_key

    def send_single_sms(self, code, mobile):
        # 发送单条短信
        url = "https://sms.yunpian.com/v2/sms/single_send.json"
        text ="【彭亚运生鲜商城】 生鲜商城 您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
        data = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": text,

        }
        res = requests.post(url, data=data)
        return res

if __name__ == "__main__":
    yun_pian = YunPian("37a35942325be7af542ca05b22aa16ab")
    res = yun_pian.send_single_sms("1234", "13720297493")
    print(res.text)
