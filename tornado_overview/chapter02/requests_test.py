import requests
headers = {
    "Content-Type": "application/x-www-form-urlencoded;",
  }
print(requests.post("http://127.0.0.1:8888/?name=bobby1", json={
    "name":"bobby2",
    "age":28
}).text)
# print(requests.get("http://127.0.0.1:8888/?name=bobby&name=bobby2"))
