# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MiyuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    miyu_type = scrapy.Field()
    question = scrapy.Field()
    answer = scrapy.Field()
    annotation = scrapy.Field()
