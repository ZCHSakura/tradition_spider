# -*- coding: utf-8 -*-
import csv
import time

import scrapy

from shaoerkepu.items import ShaoerkepuItem


class KepuSpider(scrapy.Spider):
    name = 'kepu'
    allowed_domains = ['youjiao.com']
    start_urls = ['http://www.youjiao.com/etly/kpzs/']

    def parse(self, response):
        type_Flist = response.xpath('//div[contains(@class,"main")]')
        for type_Slist in type_Flist:
            typeNames = type_Slist.xpath('.//div[@class="inbox"]')
            # 如果是右边三个的话
            if not typeNames:
                typeName = type_Slist.xpath('.//h2/a/text()').extract_first()
                typeUrl = type_Slist.xpath('.//h2/a/@href').extract_first()
                request = scrapy.Request(typeUrl, callback=self.type_detail, meta={})
                request.meta['type'] = typeName
                yield request
            else:
                for typee in typeNames:
                    typeName = typee.xpath('./h2/a/text()').extract_first()
                    typeUrl = typee.xpath('./h2/a/@href').extract_first()
                    request = scrapy.Request(typeUrl, callback=self.type_detail, meta={})
                    request.meta['type'] = typeName
                    yield request

    def type_detail(self, response):
        time.sleep(1)
        kepu_list = response.xpath('//div[@class="bk-listcon right"]/dl')
        for kepu in kepu_list:
            name = kepu.xpath('./dd/h3/a/text()').extract_first()
            detailUrl = kepu.xpath('./dd/h3/a/@href').extract_first()
            request = scrapy.Request(detailUrl, callback=self.kepu_detail, meta={'middleware': 'IngoreRequestMiddleware'})
            request.meta['type'] = response.meta['type']
            request.meta['name'] = name
            yield request

        # 翻页
        next_page = response.xpath('//a[contains(text(),"下一页")]/@href').extract_first()
        if next_page:
            next_url = next_page
            print('翻页')
            request1 = scrapy.Request(next_url, callback=self.type_detail)
            request1.meta['type'] = response.meta['type']
            yield request1

    def kepu_detail(self, response):
        item = ShaoerkepuItem()
        item['type'] = response.meta['type']
        item['name'] = response.meta['name']
        content = response.xpath('//div[@class="content ft14"]/p[last()-1]')[0].xpath('string(.)').extract_first()\
            .replace('\t', '').replace('\xa0', '').split('\r\n')
        item['content'] = [i for i in content if i != '']
        item['url'] = response.url
        if item['content'] and '幼教网整理了关于' in item['content'][0]:
            del item['content'][0]
        yield item
