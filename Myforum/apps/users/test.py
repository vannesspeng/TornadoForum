#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:pyy
# datetime:2019/1/2 15:17
import json
from random import choices

import requests

web_url = "http://127.0.0.1:8888"
def test_sms():
    url = "{}/code/".format(web_url)
    data = {
        "mobile":"13720297493"
    }
    res = requests.post(url, json=data)

    print(json.loads(res.text))

def test_register():
    url = "{}/register/".format(web_url)
    data = {
        "mobile": "13720297493",
        "code":"4259",
        "password":"admin123"
    }
    res = requests.post(url, json=data)

    print(json.loads(res.text))


def test_getgroup():
    url = "{}/users/7/groups/".format(web_url)
    res = requests.get(url)
    print(json.loads(res.text))

if __name__ == "__main__":
    # test_sms()
    test_getgroup()