import socket
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ

selector = DefaultSelector()

class Fetcher:
    def connected(self, key):
        selector.unregister(key.fd)
        self.client.send("GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n".format("/", self.host).encode("utf8"))
        selector.register(self.client.fileno(), EVENT_READ, self.readble)

    def readble(self, key):
        d = self.client.recv(1024)
        if d:
            self.data += d
        else:
            selector.unregister(key.fd)
            data = self.data.decode("utf8")
            print(data)

    def get_url(self, url):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setblocking(False)
        self.data = b""
        self.host = "www.baidu.com"

        try:
            self.client.connect((self.host, 80))  # 阻塞io， 意味着这个时候cpu是空闲的
        except BlockingIOError as e:
            # 做一些其他事
            pass

        selector.register(self.client.fileno(), EVENT_WRITE, self.connected)

def loop_forever():
    #事件循环
    while 1:
        ready = selector.select()
        for key, mask in ready:
            call_back = key.data
            call_back(key)

if __name__ == "__main__":
    fetcher = Fetcher()
    url = "http://www.baidu.com"
    fetcher.get_url(url)
    loop_forever()


