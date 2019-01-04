#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:pyy
# datetime:2018/12/28 15:18
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

settings = {
    "static_path": os.path.join(BASE_DIR, "media"),
    "static_url_prefix": "/static/",
    "template_path": "templates",
    'MEDIA_ROOT': os.path.join(BASE_DIR, "media"),
    "SITE_URL":"http://127.0.0.1:8888",
    "db": {
        "host": "127.0.0.1",
        "user": "root",
        "password": "root",
        "name": "message",
        "port": 3306
    },
    "redis": {
        "host":"127.0.0.1"
    }

}
