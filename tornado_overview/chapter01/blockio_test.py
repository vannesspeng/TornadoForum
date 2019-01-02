#阻塞io
import requests
# html = requests.get("http://www.baidu.com").text
# #1. 三次握手建立tcp连接，
# # 2. 等待服务器响应
# print(html)

#如何通过socket直接获取html
import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "www.baidu.com"
client.connect((host, 80))  #阻塞io， 意味着这个时候cpu是空闲的
client.send("GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n".format("/", host).encode("utf8"))

data = b""
while 1:
    d = client.recv(1024) #阻塞直到有數據
    if d:
        data += d
    else:
        break

data = data.decode("utf8")
print(data)





