# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    name = scrapy.Field()
    img = scrapy.Field()
    intro = scrapy.Field()


class ChapterItem(scrapy.Item):
    book_name = scrapy.Field()
    chapter_title = scrapy.Field()
    chapter_name = scrapy.Field()
    content = scrapy.Field()
    # 译文和段译
    translation = scrapy.Field()
    # 注释
    annotation = scrapy.Field()
    # 按语
    note = scrapy.Field()
