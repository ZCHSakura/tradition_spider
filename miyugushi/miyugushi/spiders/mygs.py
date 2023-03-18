# -*- coding: utf-8 -*-
import scrapy

from miyugushi.items import MiyugushiItem


class MygsSpider(scrapy.Spider):
    name = 'mygs'
    allowed_domains = ['cmiyu.com']
    start_urls = ['http://www.cmiyu.com/mygs/list491.html']

    def parse(self, response):
        gushi_list = response.xpath('//div[@class="list"]/ul/li')
        for gushi in gushi_list:
            name = gushi.xpath('./a/text()').extract_first()
            if not name:
                name = gushi.xpath('./a/b/text()').extract_first()
            info_page = gushi.xpath('./a/@href').extract_first()
            # 向内翻页
            if info_page:
                next_url = 'http://www.cmiyu.com' + info_page
                request = scrapy.Request(next_url, callback=self.gushi_info)
                request.meta['name'] = name
                yield request
            else:
                print('我不对')

        # 翻页
        next_page = response.xpath('//li[@class="sy3"]/a[contains(text(), "下一页")]/@href').extract_first()
        if next_page:
            next_url = 'http://www.cmiyu.com/mygs/' + next_page
            yield scrapy.Request(next_url, callback=self.parse)

    def gushi_info(self, response):
        item = MiyugushiItem()
        item['name'] = response.meta['name']
        item['annotation'] = response.xpath('//div[@class="zy"]/p/text()').extract_first()
        text = response.xpath('//div[@class="myjsmd"]')
        content = text[0].xpath('string(.)').extract_first()\
            .replace(' ', '').replace('\t', '').replace('\xa0', '').split('\r\n')
        item['content'] = [i for i in content if i != '']
        yield item
