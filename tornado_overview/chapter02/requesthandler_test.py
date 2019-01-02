import json
from tornado.web import RequestHandler

class MainHandler(RequestHandler):
    #入口
    # def initialize(self, db):
    #     #用于初始化handler类的过程
    #     self.db = db

    def prepare(self):
        #prepare方法用于真正调用请求处理之前的初始化方法
        #1. 打印日志， 打开文件
        pass

    def on_finish(self):
        #关闭句柄， 清理内存
        pass


    #http方法
    def get(self, *args, **kwargs):
        # data1 = self.get_query_argument("name")
        # data2 = self.get_query_arguments("name")
        data1 = self.get_argument("name")
        data2 = self.get_arguments("name")
        self.redirect("", permanent=True)
        pass


    def post(self, *args, **kwargs):
        # data1 = self.request.arguments
        # data2 = self.get_arguments("name")
        # param = self.request.body.decode("utf8")
        # data1 = json.loads(param)
        # try:
        #     data1 = self.get_body_argument("name")
        #     data2 = self.get_body_arguments("name")
        # except Exception as e:
        #     self.set_status(500)
        self.finish({
            "name":"bobby"
        })
    def delete(self, *args, **kwargs):
        pass
    def patch(self, *args, **kwargs):
        pass

    def write_error(self, status_code, **kwargs):
        pass

    #输出
    #1. set_status, write, finish, redirect, write_error

import tornado
urls = [
    tornado.web.URLSpec("/", MainHandler, name="index"),
]

if __name__ == "__main__":
    from tornado import web
    app = web.Application(urls, debug=True)
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()