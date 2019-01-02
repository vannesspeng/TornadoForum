import asyncio

from chapter04.models.model import Goods
from chapter04.models.model import objects


async def handler():
    # await objects.create(Goods, supplier_id=7, name="53度水井坊臻酿八號500ml",
    #                      click_num=20, goods_num=1000, price=500, brief="州茅台酒厂（集团）保健酒业有限公司生产")
    goods = await objects.execute(Goods.select())
    for good in goods:
        print(good.name)

loop = asyncio.get_event_loop()
loop.run_until_complete(handler())
# loop.close()
