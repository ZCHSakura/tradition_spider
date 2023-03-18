# -*- coding: utf-8 -*-
import re

import scrapy

from zhuanlan.items import gongyiItem


class GongyiSpider(scrapy.Spider):
    name = 'gongyi'
    allowed_domains = ['rouding.com']
    start_urls = ['https://www.rouding.com/minjianyishu/']

    def parse(self, response):
        themeList = response.xpath('//div[@class="topcd"]/ul/li[not(@class="this")]')
        for themee in themeList:
            theme = themee.xpath('./a/text()').get()
            themeUrl = themee.xpath('./a/@href').get()
            yield scrapy.Request(themeUrl, callback=self.infoList, meta={'theme': theme})

    def infoList(self, response):
        itemList = response.xpath('//div[@class="all"]/div')
        for item in itemList:
            name = item.xpath('./a/div[@class="x7"]/text()').get()
            cover = 'https:' + re.findall(r'[(](.*?)[)]', item.xpath('./a/div[@class="x6"]/@style').get())[0]
            infoUrl = 'https:' + item.xpath('./a/@href').get()
            yield scrapy.Request(infoUrl, callback=self.infoDetail, meta={'theme': response.meta['theme'],
                                                                           'name': name, 'cover': cover})

        # 翻页
        next_url = response.xpath('//div[@class="list_fy bg"]/a[last()-1]/@href').extract_first()
        if next_url and next_url != '#':
            yield scrapy.Request(next_url, callback=self.infoList, meta={'theme': response.meta['theme']})

    def infoDetail(self, response):
        item = gongyiItem()
        item['theme'] = response.meta['theme']
        item['name'] = response.meta['name']
        item['cover'] = response.meta['cover']
        item['author'] = re.findall(r'作者：(.*?) /', response.xpath('//div[@class="list2"]')[0].xpath('string(.)').get())[0]
        item['modifiedTime'] = re.findall(r'时间：(.*?) /', response.xpath('//div[@class="list2"]')[0].xpath('string(.)').get())[0]
        content = response.xpath('//div[@class="ct tt zooms"]')[0].getall()[0]
        item['content'] = re.sub(r'href="([^"])*[^=k]"', "", content)
        yield item
