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


def get_message():
    res = requests.get("{}/messages/".format(web_site_url), headers=headers)
    print(res.status_code)
    print(json.loads(res.text))

if __name__ == "__main__":
    get_message()