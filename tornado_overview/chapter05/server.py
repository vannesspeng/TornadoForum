# 1. 什么是模板
from tornado.web import StaticFileHandler, RedirectHandler
from aiomysql import create_pool
# 1. RedirectHandler
# 1. 301是永久重定向， 302是临时重定向，获取用户个人信息， http://www.baidu.com https

# StaticFileHandler
import time

from tornado import web
import tornado
from tornado.web import template
from chapter05.forms import MessageForm
from chapter05.models import Message

class MainHandler(web.RequestHandler):
    def initialize(self, db):
        self.db = db

    async def get(self, *args, **kwargs):
        message_from = MessageForm()
        self.render("message.html", message_form=message_from)

    async def post(self, *args, **kwargs):
        message_from = MessageForm(self.request.arguments)
        if message_from.validate():
            #验证通过， 获取具体的值并保存
            name = message_from.name.data
            email = message_from.email.data
            address = message_from.address.data
            message_data = message_from.message.data

            message = Message()
            message.name = name
            message.email = email
            message.address = address
            message.message = message_data

            message.save()

            self.render("message.html", message_form=message_from)
        else:
            self.render("message.html", message_form=message_from)


settings = {
    "static_path": "C:/projects/tornado_overview/chapter03/static",
    "static_url_prefix": "/static/",
    "template_path": "templates",
    "db": {
        "host": "127.0.0.1",
        "user": "root",
        "password": "root",
        "name": "message",
        "port": 3306
    }
}

if __name__ == "__main__":
    app = web.Application([
        ("/", MainHandler, {"db": settings["db"]}),
        # ("/static/(.*)", StaticFileHandler, {"path": "C:/projects/tornado_overview/chapter03/static"})
    ], debug=True, **settings)
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

# self.redirect方法和RedirectHandler方法区别是什么
# self.redirect
