# -*- coding: utf-8 -*-
import re

import scrapy

from zhuanlan.items import minsuItem


class MinsuSpider(scrapy.Spider):
    name = 'minsu'
    allowed_domains = ['3cwm.com']
    start_urls = ['http://www.3cwm.com/channel.asp?id=21&*1-1-0&url?www.3cwm.com-0*1-1-0.html']

    def parse(self, response):
        infoList= response.xpath('//div[@class="bb1"][1]/div[@class="ys10 link4"]')
        for info in infoList:
            name = info.xpath('./div[@class="ys10_2 fr"]/a/text()').get()
            detailUrl = info.xpath('./div[@class="ys10_2 fr"]/a/@href').get()
            if detailUrl:
                yield scrapy.Request(detailUrl, callback=self.infoDetail, meta={'name': name})
        # 翻页
        if response.xpath('//div[@class="bb1"][1]/div[last()]/div/span[last()-1]/a/text()').get() == '下一页':
            next_page = response.xpath('//div[@class="bb1"][1]/div[last()]/div/span[last()-1]/a/@href').get()
            yield scrapy.Request(next_page, callback=self.parse)

    def infoDetail(self, response):
        item = minsuItem()
        item['name'] = response.meta['name']
        item['author'] = re.findall(r'作者：(.*?)\xa0', response.xpath('//div[@class="c3 link1"]/text()').get())[0]
        content = response.xpath('//div[@class="center line4"]')[0].getall()[0]
        item['content'] = re.sub(r'href="([^"]*?)"', "", content).replace('src="/', 'src="http://www.3cwm.com/')
        yield item

