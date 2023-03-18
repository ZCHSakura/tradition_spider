# -*- coding: utf-8 -*-
import scrapy

from zhenbaoguan.items import ZhenbaoguanItem


class ShuhuaSpider(scrapy.Spider):
    name = 'shuhua'
    allowed_domains = ['ltfc.net']
    start_urls = ['http://ltfc.net/exhibit/essence']

    def parse(self, response):
        shuhua_list = response.xpath('//div[@class="row" and not(@id)]/div')
        for shuhua in shuhua_list:
            item = ZhenbaoguanItem()
            item['name'] = shuhua.xpath('./div/div/h4/a/text()').get().replace('\n', '').replace(' ', '')
            if shuhua.xpath('./div/a/img/@src').get():
                item['img'] = shuhua.xpath('./div/a/img/@src').get()
            item['content_url'] = 'http://ltfc.net' + shuhua.xpath('./div/a/@href').get()
            item['content'] = None
            item['dynasty'] = shuhua.xpath('./div/div/p[1]/text()').get().split(' ')[0]
            item['author'] = shuhua.xpath('./div/div/p[1]/text()').get().split(' ')[1]
            item['size'] = shuhua.xpath('./div/div/p[1]/span/text()').get()
            item['pixel'] = shuhua.xpath('./div/div/p[2]/text()').get()
            item['intro'] = shuhua.xpath('./div/div/p[last()]/text()').get()
            yield item

