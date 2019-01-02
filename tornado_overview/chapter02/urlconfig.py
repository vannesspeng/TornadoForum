import time

from tornado import web
import tornado

class MainHandler(web.RequestHandler):
    #当客户端发起不同的http方法的时候,只需要重载handler中的对应的方法即可
    async def get(self, *args, **kwargs):
        self.write("hello world")

class PeopleIdHandler(web.RequestHandler):
    def initialize(self, name):
        self.db_name = name

    async def get(self, id, *args, **kwargs):
        self.redirect("用户id:{}".format(id))
        # self.redirect(self.reverse_url("people_name", "bobby"))

class PeopleNameHandler(web.RequestHandler):
    async def get(self, name, *args, **kwargs):
        self.write("用户姓名:{}".format(name))

class PeopleInfoHandler(web.RequestHandler):
    async def get(self, name, age, gender, *args, **kwargs):
        self.write("用户姓名:{},用户年龄:{},用户性别:{},".format(name, age, gender))

people_db = {
    "name":"people"
}
from tornado.web import url
#配置如/people/1/
urls = [
    tornado.web.URLSpec("/", MainHandler, name="index"),
    tornado.web.URLSpec("/people/(\d+)/?", PeopleIdHandler, people_db, name="people_id"),
    tornado.web.URLSpec("/people/(\w+)/?", PeopleNameHandler, name="people_name"), #配置如/people/bobby/
    # tornado.web.URLSpec("/people/(\w+)/(\d+)/(\w+)/?", PeopleInfoHandler, name="people_info"), #配置如/people/name/age/gender/
    tornado.web.URLSpec("/people/(?P<name>\w+)/(?P<age>\d+)/(?P<gender>\w+)/?", PeopleInfoHandler, name="people_info"), #配置如/people/name/age/gender/
]

if __name__ == "__main__":
    app = web.Application(urls, debug=True)
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

#1.url的各种参数配置
#2. url命名 reverse_url
#3. 给handler传入初始值
