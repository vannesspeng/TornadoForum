#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:pyy
# datetime:2019/2/14 10:36
import json
from datetime import datetime
import requests
import jwt

from Myforum.Forum.settings import settings

current_time = datetime.utcnow()

web_site_url = "http://127.0.0.1:8888"
data = jwt.encode({
    "name":"vanness",
    "id":7,
    "exp":current_time
}, settings["secret_key"]).decode("utf8")

headers={
        "tsessionid":data
    }


def new_question():
    files = {
        "image":open("D:/images/python.png", "rb")
    }
    data = {
        "title": "tornado问题",
        "content": "这里是学前教育的交流中心，大家有什么问题可以一起来交流讨论！欢迎大家的加入！",
        "category": "技术问答"
    }
    res = requests.post("{}/questions/".format(web_site_url), headers=headers, data=data, files=files)
    print(res.status_code)
    print(json.loads(res.text))

def get_question():
    res = requests.get("{}/questions/".format(web_site_url), headers=headers)
    print(res.status_code)
    print(json.loads(res.text))

def add_answer(question_id):
    data = {
        "content": "不可以，xadmin是django框架使用的"
    }
    res = requests.post("{}/questions/{}/answers/".format(web_site_url, question_id), headers=headers, json=data)
    print(res.status_code)
    print(json.loads(res.text))

if __name__ == "__main__":

    # 新建问题
    # new_question()
    # get_question()
    add_answer(2)