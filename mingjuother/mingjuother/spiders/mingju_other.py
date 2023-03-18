# -*- coding: utf-8 -*-
import scrapy

from mingjuother.items import MingjuotherItem


class MingjuOtherSpider(scrapy.Spider):
    name = 'mingju_other'
    allowed_domains = ['so.gushiwen.org']
    start_urls = ['https://so.gushiwen.org/mingju/Default.aspx?p=1&c=%e9%a3%9f%e7%89%a9&t=%e8%8d%94%e6%9e%9d']

    def parse(self, response):
        item = MingjuotherItem()
        mingjuju_list = response.xpath('//div[@class="sons" and @style=" padding-bottom:12px;"]/div[@class="cont"]')
        for mingju in mingjuju_list:
            item['come_from'] = mingju.xpath('.//a[@target="_blank" and @style=" float:left;"][2]/text()') \
                .extract_first()
            item['content'] = mingju.xpath('./a[@style=" float:left;"][1]/text()').extract_first()
            item['theme'] = response.xpath('//div[@style="border-bottom:0px;padding-bottom:0px;"]/div[@class="sright"]'
                                           '/span/text()').extract_first()
            item['classify'] = response.xpath('//div[@style=" border:0px; margin-top:0px;"]/div[@class="sright"]'
                                              '/span/text()').extract_first()
            yield item

        # 翻页
        next_page = response.xpath('//a[@class="amore"]/@href').extract_first()
        if next_page:
            next_url = 'https://so.gushiwen.org' + next_page
            yield scrapy.Request(next_url, callback=self.parse)

