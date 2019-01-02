from datetime import datetime

from peewee import *
from peewee import Model
import peewee_async

db = MySQLDatabase('message', host="127.0.0.1", port=3306, user="root", password="root")

database = peewee_async.MySQLDatabase(
    'message', host="127.0.0.1", port=3306, user="root", password="root"
)

objects = peewee_async.Manager(database)

# No need for sync anymore!


database.set_allow_sync(False)


class BaseModel(Model):
    add_time = DateTimeField(default=datetime.now, verbose_name="添加时间")
    class Meta:
        database = database

class Supplier(BaseModel):
    name = CharField(max_length=100, verbose_name="名称", index=True)
    address = CharField(max_length=100, verbose_name="联系地址")
    phone = CharField(max_length=11, verbose_name="联系方式")
    class Meta:
        database = db
        table_name = "supplier"

class Goods(BaseModel):
    supplier = ForeignKeyField(Supplier, verbose_name="商家", backref="goods")
    name = CharField(max_length=100, verbose_name="商品名称", index=True)
    click_num = IntegerField(default=0, verbose_name="点击数")
    goods_num = IntegerField(default=0, verbose_name="库存数")
    price = FloatField(default=0.0, verbose_name="价格")
    brief = TextField(verbose_name="商品简介")

    class Meta:
        table_name = "goods"


def init_table():
    db.create_tables([Goods, Supplier])
if __name__ == "__main__":
    init_table()