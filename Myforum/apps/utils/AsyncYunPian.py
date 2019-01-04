#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:pyy
# datetime:2019/1/2 9:26
import json
from functools import partial
from urllib.parse import urlencode
import tornado
from tornado import httpclient
from tornado.httpclient import HTTPRequest


class AsyncYunPian:
    def __init__(self, api_key):
        self.api_key = api_key

    async def send_single_sms(self, code, mobile):
        # 发送单条短信
        # 这里使用tornado框架中的httpclient来发送网络请求
        http_client = httpclient.AsyncHTTPClient()
        url = "https://sms.yunpian.com/v2/sms/single_send.json"
        text ="【彭亚运生鲜商城】 生鲜商城 您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)

        post_request = HTTPRequest(url=url, method="POST", body=urlencode({
            "apikey": self.api_key,
            "mobile": mobile,
            "text": text,
        }))
        res = await http_client.fetch(post_request)
        return json.loads(res.body.decode("utf8"))

if __name__ == "__main__":
    # 使用事件循环
    io_loop = tornado.ioloop.IOLoop.current()
    yun_pian = AsyncYunPian("37a35942325be7af542ca05b22aa16ab")
    # 将send_single_sms函数和它的参数包装成一个新的函数new_func，这里使用的是partial函数
    new_func = partial(yun_pian.send_single_sms, "1234", "13720297493")
    # 使用事件循环的run_sync方法，该方法在协程运行完毕后，会自动结束事件循环
    io_loop.run_sync(new_func)
