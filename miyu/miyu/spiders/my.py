# -*- coding: utf-8 -*-
import scrapy

from miyu.items import MiyuItem


class MySpider(scrapy.Spider):
    name = 'my'
    allowed_domains = ['cmiyu.com']
    start_urls = ['http://www.cmiyu.com/qtmy/']

    def parse(self, response):
        miyu_type = response.xpath('//div[@class="weizhi"]/a[2]/text()').extract_first()
        miyu_list = response.xpath('//div[@class="list"]/ul/li')
        for miyu in miyu_list:
            question = miyu.xpath('./a/text()').extract_first()
            if not question:
                question = miyu.xpath('./a/b/text()').extract_first()
            info_page = miyu.xpath('./a/@href').extract_first()
            # 向内翻页
            if info_page:
                next_url = 'http://www.cmiyu.com' + info_page
                request = scrapy.Request(next_url, callback=self.miyu_info)
                request.meta['miyu_type'] = miyu_type
                request.meta['question'] = question
                yield request
            else:
                print('我不对')

        # 翻页
        next_page = response.xpath('//li[@class="sy3"]/a[contains(text(), "下一页")]/@href').extract_first()
        if next_page:
            next_url = 'http://www.cmiyu.com/' + response.xpath('//div[@class="weizhi"]/a[2]/@href').extract_first() \
                       + next_page
            yield scrapy.Request(next_url, callback=self.parse)

    def miyu_info(self, response):
        item = MiyuItem()
        item['miyu_type'] = response.meta['miyu_type']
        item['question'] = response.meta['question']
        item['answer'] = response.xpath('//div[@class="md"]/h3[2]/text()').extract_first()\
            .replace('谜底：', '').replace('\r', '').replace('\n', '')
        item['annotation'] = response.xpath('//div[@class="zy"]/p/text()').extract_first()
        if item['annotation']:
            item['annotation'] = item['annotation'].replace('\r', '').replace('\n', '')
        if not item['miyu_type']:
            print('有个空的type')
        if not item['answer']:
            print('有个空的answer')
            answer = response.xpath('//div[@class="md"]/h3[2]')
            item['answer'] = answer[0].xpath('string(.)').extract_first().replace('谜底：', '')
            print(item['answer'])
        if not item['question']:
            print('有个空的question')
        print(item)
        yield item
