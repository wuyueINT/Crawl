# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Crawl02Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# 定义存放网页信息的数据结构
class ShfairItems(scrapy.Item):
    # item中只有一种Field类型，这种类型可以接受所有存储类型的数据
    type = scrapy.Field()
    company_cn = scrapy.Field()
    company_en = scrapy.Field()
    number = scrapy.Field()
    image = scrapy.Field()
    image_path = scrapy.Field()
    url_md5 = scrapy.Field()
