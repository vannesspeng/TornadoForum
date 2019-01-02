#define, options

import time
from tornado import web
import tornado
from tornado.options import define, options, parse_command_line

#define， 定义一些可以在命令行中传递的参数以及类型
define('port', default=8008, help="run on the given port", type=int)
define('debug', default=True, help="set tornado debug mode", type=bool)

# options.parse_command_line()
options.parse_config_file("conf.cfg")

#options是一个类，全局只有一个options

class MainHandler(web.RequestHandler):
    #当客户端发起不同的http方法的时候， 只需要重载handler中的对应的方法即可
    async def get(self, *args, **kwargs):
        self.write("hello world")

class MainHandler2(web.RequestHandler):
    #当客户端发起不同的http方法的时候， 只需要重载handler中的对应的方法即可
    async def get(self, *args, **kwargs):
        self.write("hello world2")

if __name__ == "__main__":
    app = web.Application([
        ("/", MainHandler),
        ("/2/", MainHandler2)
    ], debug=options.debug)
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
