#1. 什么是模板
from tornado.web import StaticFileHandler, RedirectHandler

#1. RedirectHandler
#1. 301是永久重定向， 302是临时重定向，获取用户个人信息， http://www.baidu.com https

#StaticFileHandler
import time

from tornado import web
import tornado
from tornado.web import template

class MainHandler(web.RequestHandler):
    #当客户端发起不同的http方法的时候， 只需要重载handler中的对应的方法即可
    async def get(self, *args, **kwargs):
        #web框架都会有模板功能
        #django和tornado对于模板的思路或者理念是完全不一样的
        orders = [
            {
                "name":"小米T恤 忍者米兔双截棍 军绿 XXL",
                "image":"http://i1.mifile.cn/a1/T11lLgB5YT1RXrhCrK!40x40.jpg",
                "price":39,
                "nums":3,
                "detail":"<a href='http://www.baidu.com'>查看详情</a>"
            },
            {
                "name": "招财猫米兔 白色",
                "image": "http://i1.mifile.cn/a1/T14BLvBKJT1RXrhCrK!40x40.jpg",
                "price": 49,
                "nums": 2,
                "detail": "<a href='http://www.baidu.com'>查看详情</a>"
            },
            {
                "name": "小米圆领纯色T恤 男款 红色 XXL",
                "image": "http://i1.mifile.cn/a1/T1rrDgB4DT1RXrhCrK!40x40.jpg",
                "price": 59,
                "nums": 1,
                "detail": "<a href='http://www.baidu.com'>查看详情</a>"
            }
        ]
        self.render("index.html", orders=orders)

class MainHandler2(web.RequestHandler):
    #当客户端发起不同的http方法的时候， 只需要重载handler中的对应的方法即可
    async def get(self, *args, **kwargs):
        self.write("hello world2")

settings = {
    "static_path":"C:/projects/tornado_overview/chapter02/static",
    "static_url_prefix":"/static2/",
    "template_path": "templates"
}

if __name__ == "__main__":
    app = web.Application([
        ("/", MainHandler),
        ("/2/", RedirectHandler, {"url":"/"}),
        ("/static/(.*)", StaticFileHandler, {"path": "C:/projects/tornado_overview/chapter02/static"})
    ], debug=True, **settings)
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

#self.redirect方法和RedirectHandler方法区别是什么
#self.redirect




