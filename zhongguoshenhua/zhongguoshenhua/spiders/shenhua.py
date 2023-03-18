# -*- coding: utf-8 -*-
import scrapy

from zhongguoshenhua.items import ZhongguoshenhuaItem


class ShenhuaSpider(scrapy.Spider):
    name = 'shenhua'
    allowed_domains = ['gs5000.cn']
    start_urls = ['http://www.gs5000.cn/gs/shenhua/']

    def parse(self, response):
        shenhua_list = response.xpath('//div[@class="listbox1"]/ul/li')
        for shenhua in shenhua_list:
            name = shenhua.xpath('./a[2]')[0].xpath('string(.)').extract_first()
            img = 'http://www.gs5000.cn'+shenhua.xpath('./a[1]/img/@src').extract_first()
            info_url = 'http://www.gs5000.cn'+shenhua.xpath('./a[1]/@href').extract_first()
            request = scrapy.Request(info_url, callback=self.shenhua_info)
            request.meta['name'] = name
            request.meta['img'] = img
            yield request

        # 翻页
        next_page = response.xpath('//a[contains(text(), "下一页")]/@href').extract_first()
        if next_page:
            next_url = 'http://www.gs5000.cn/gs/shenhua/' + next_page
            yield scrapy.Request(next_url, callback=self.parse)

    def shenhua_info(self, response):
        item = ZhongguoshenhuaItem()
        item['name'] = response.meta['name']
        item['img'] = response.meta['img']
        content = response.xpath('//div[@class="content"]/table[1]/tr/td')[0].xpath('string(.)').extract_first()\
            .replace('\xa0\r\n', '').split('\r\n')
        item['content'] = [i for i in content if i != '' and i != '\u3000\u3000']
        yield item
