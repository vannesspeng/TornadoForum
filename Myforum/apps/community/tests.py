#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:pyy
# datetime:2019/1/9 14:01
import json

import requests
web_site_url = "http://127.0.0.1:8888"
tesssionid = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Nywibmlja25hbWUiOm51bGwsImV4cCI6MTU0NzAyMTQ1NH0.P3x5XMQKgGvlSehGTn1w7rPPKdKTtqvnhm4odBVldUA"
headers = {"tesssionid": tesssionid}

# requests.get(url=web_site_url, headers=headers)


def create_group():
    files = {
        "front_image": open("D:/images/python.png", "rb")
    }
    data = {
        "name": "学前教育交流角",
        "desc": "这里是学前教育的交流中心，大家有什么问题可以一起来交流讨论！欢迎大家的加入！",
        "notice": "这里是学前教育的交流中心，大家有什么问题可以一起来交流讨论！欢迎大家的加入！",
        "category": "教育同盟"
    }
    res = requests.post("{}/groups/".format(web_site_url), headers=headers, data=data, files=files)
    print(res.status_code)
    print(json.loads(res.text))

if __name__ == "__main__":
    create_group()