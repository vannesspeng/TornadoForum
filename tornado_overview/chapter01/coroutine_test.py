#1. 什么是协程
#1.回调过深造成代码很难维护
#2.栈撕裂造成异常无法向上抛出
#协程- 可以被暂停并切换到其他协程运行的函数
from tornado.gen import coroutine

async def yield_test():
    yield 1
    yield 2
    yield 3

async def main():
    result = await yield_test()
    result = await yield_test2()

async def main2():
    await yield_test()

my_yield = yield_test()
for item in my_yield:
    print(item)