# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class yangshengItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    typeName = scrapy.Field()
    name = scrapy.Field()
    content = scrapy.Field()

class gongyiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    theme = scrapy.Field()
    name = scrapy.Field()
    cover = scrapy.Field()
    author = scrapy.Field()
    modifiedTime = scrapy.Field()
    content = scrapy.Field()

class minsuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
