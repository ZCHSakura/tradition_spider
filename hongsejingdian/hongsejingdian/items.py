# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HongsejingdianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    province = scrapy.Field()
    img = scrapy.Field()
    imgList = scrapy.Field()
    level = scrapy.Field()
    location = scrapy.Field()
    phone = scrapy.Field()
    content = scrapy.Field()
