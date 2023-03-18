# -*- coding: utf-8 -*-
import scrapy

from xiehouyu.items import XiehouyuItem


class XhySpider(scrapy.Spider):
    name = 'xhy'
    allowed_domains = ['xhy.5156edu.com']
    start_urls = ['http://xhy.5156edu.com/html2/xhy.html']

    def parse(self, response):
        item = XiehouyuItem()
        question_list = response.xpath('//tr[@bgcolor="#ffffff"]')
        for question in question_list:
            item['question'] = question.xpath('./td[1]/text()').extract_first()
            item['answer'] = question.xpath('./td[2]/text()').extract_first()
            yield item

        # 翻页
        next_page = response.xpath('//a[contains(text(), "下一页")]/@href').extract_first()
        if next_page:
            next_url = 'http://xhy.5156edu.com/' + next_page
            yield scrapy.Request(next_url, callback=self.parse)
