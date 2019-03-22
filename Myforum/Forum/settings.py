#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:pyy
# datetime:2018/12/28 15:18
import os

import peewee_async

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

settings = {
    "static_path": os.path.join(BASE_DIR, "media"),
    "static_url_prefix": "/static/",
    "template_path": "templates",
    "secret_key": "ZGGA#Mp4yL4w5CDu",
    "jwt_expire": 7 * 24 * 3600,
    'MEDIA_ROOT': os.path.join(BASE_DIR, "media"),
    "SITE_URL": "http://127.0.0.1:8888",
    "db": {
        "host": "127.0.0.1",
        "user": "root",
        "password": "root",
        "name": "myforum",
        "port": 3306
    },
    "redis": {
        "host": "127.0.0.1"
    },
    "LOCALHOST_URL": "http://127.0.0.1:8888"
}

database = peewee_async.MySQLDatabase(
    'myforum', host="127.0.0.1", port=3306, user="root", password="root"
)
