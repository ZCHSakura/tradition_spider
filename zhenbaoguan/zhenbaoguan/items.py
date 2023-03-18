# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhenbaoguanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    img = scrapy.Field()
    content_url = scrapy.Field()
    content = scrapy.Field()
    dynasty = scrapy.Field()
    author = scrapy.Field()
    size = scrapy.Field()
    # 像素
    pixel = scrapy.Field()
    intro = scrapy.Field()
