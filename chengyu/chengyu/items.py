# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ChengyuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    # 读音
    pronunciation = scrapy.Field()
    # 释义
    explanation = scrapy.Field()
    # 出处
    provenance = scrapy.Field()
