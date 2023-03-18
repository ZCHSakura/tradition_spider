# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YishuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category = scrapy.Field()
    name = scrapy.Field()
    cover = scrapy.Field()
    author = scrapy.Field()
    intro = scrapy.Field()

class ChapterItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    bookName = scrapy.Field()
    chapterTitleNum = scrapy.Field()
    chapterTitle = scrapy.Field()
    chapterNameNum = scrapy.Field()
    chapterName = scrapy.Field()
    haveContent = scrapy.Field()
    content = scrapy.Field()
