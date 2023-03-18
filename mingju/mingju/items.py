# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MingjuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    book_name = scrapy.Field()
    chapter_title = scrapy.Field()
    chapter_name = scrapy.Field()
    content = scrapy.Field()
    # 翻译
    translation = scrapy.Field()
