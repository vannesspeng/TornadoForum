#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:pyy
# datetime:2019/1/9 11:34
from datetime import datetime

import jwt

from Myforum.Forum.settings import settings

current_time = datetime.utcnow()

data = jwt.encode({
    "name":"bobby",
    "id":1,
    "exp":current_time
}, "abc").decode("utf8")

import time
time.sleep(2)

data = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Nywibmlja25hbWUiOm51bGwsImV4cCI6MTU0NzAyMTQ1NH0.P3x5XMQKgGvlSehGTn1w7rPPKdKTtqvnhm4odBVldUA"
send_data = jwt.decode(data, settings["secret_key"], leeway=1, options={"verify_exp":False})

print(send_data)