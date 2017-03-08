# coding: utf-8
from scrapy.item import Item, Field

class DoubanItem(Item):
    # define the fields for your item here like:
    # name = Field()
    groupname = Field()
    groupurl = Field()
    totalnumber = Field()