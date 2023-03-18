# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhougongjiemengItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    dream_type = scrapy.Field()
    theme = scrapy.Field()
    content = scrapy.Field()
