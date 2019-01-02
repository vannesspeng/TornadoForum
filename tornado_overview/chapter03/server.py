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


class MainHandler(web.RequestHandler):
    def initialize(self, db):
        self.db = db

    async def get(self, *args, **kwargs):
        id = ""
        name = ""
        email = ""
        address = ""
        message = ""
        async with create_pool(host=self.db["host"], port=self.db["port"],
                               user=self.db["user"], password=self.db["password"],
                               db=self.db["name"], charset="utf8") as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT id, name, email, address, message from message")
                    try:
                        id, name, email, address, message = await cur.fetchone()
                    except Exception as e:
                        pass
        self.render("message.html", id=id, email=email, name=name, address=address, message=message)

    async def post(self, *args, **kwargs):
        id = self.get_body_argument("id", "")
        name = self.get_body_argument("name", "")
        email = self.get_body_argument("email", "")
        address = self.get_body_argument("address", "")
        message = self.get_body_argument("message", "")

        async with create_pool(host=self.db["host"], port=self.db["port"],
                               user=self.db["user"], password=self.db["password"],
                               db=self.db["name"], charset="utf8") as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    if not id:
                        await cur.execute(
                            "INSERT INTO message(name, email, address, message) VALUES('{}','{}','{}','{}')".format(name,
                                                                                                                    email,
                                                                                                                    address,
                                                                                                                    message))
                    else:
                        await cur.execute("update message set name='{}', email='{}', address='{}', message='{}'".format(name, email, address, message))
                    await conn.commit()
        self.render("message.html", id=id, email=email, name=name, address=address, message=message)


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
        ("/static/(.*)", StaticFileHandler, {"path": "C:/projects/tornado_overview/chapter03/static"})
    ], debug=True, **settings)
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

# self.redirect方法和RedirectHandler方法区别是什么
# self.redirect
