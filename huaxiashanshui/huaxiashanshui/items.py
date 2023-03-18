# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HuaxiashanshuiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    img = scrapy.Field()
    level = scrapy.Field()
    province = scrapy.Field()
    location = scrapy.Field()
    opening = scrapy.Field()
    content = scrapy.Field()
