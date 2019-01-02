from tornado import httpclient
#
# http_client = httpclient.AsyncHTTPClient()
# try:
#     response = http_client.fetch("http://www.tornadoweb.org/en/stable/")
#     print(response.body.decode("utf8"))
# except httpclient.HTTPError as e:
#     # HTTPError is raised for non-200 responses; the response
#     # can be found in e.response.
#     print("Error: " + str(e))
# except Exception as e:
#     # Other errors are possible, such as IOError.
#     print("Error: " + str(e))
# http_client.close()

async def f():
    http_client = httpclient.AsyncHTTPClient()
    try:
        response = await http_client.fetch("http://www.tornadoweb.org/en/stable/")
    except Exception as e:
        print("Error: %s" % e)
    else:
        print(response.body.decode("utf8"))

if __name__ == "__main__":
    import tornado
    io_loop = tornado.ioloop.IOLoop.current()

    #run_sync方法可以在运行完某个协程之后停止事件循环
    io_loop.run_sync(f)