# -*- coding: utf-8 -*-
import time

import scrapy
from lxml import etree

from huaxiashanshui.items import HuaxiashanshuiItem


class HuaxiaSpider(scrapy.Spider):
    name = 'huaxia'
    allowed_domains = ['cncn.com']
    start_urls = ['https://www.cncn.com/piao/all/cec4bbafd7dabdcc']

    def parse(self, response):
        place_list = response.xpath('//div[@class="list_box"]')
        for place in place_list:
            name = place.xpath('.//div[@class="title"]/a/strong/text()').extract_first()
            img = 'https:' + place.xpath('.//div[@class="list_top"]/a/img/@src').extract_first()
            level = place.xpath('.//div[@class="title"]/b/text()').extract_first()
            # location = place.xpath('.//div[@class="title"]/p[1]/text()').extract_first()
            detail_url = 'https://www.cncn.com/' + place.xpath('.//div[@class="list_top"]/a/@href').extract_first()
            request = scrapy.Request(detail_url, callback=self.place_info)
            request.meta['name'] = name
            request.meta['img'] = img
            request.meta['level'] = level
            yield request

        # 翻页
        time.sleep(2)
        next_page = response.xpath('//li[@class="next"]/a/@href').extract_first()
        print(next_page)
        if next_page:
            next_url = 'https://www.cncn.com' + next_page
            yield scrapy.Request(next_url, callback=self.parse)

    def place_info(self, response):
        item = HuaxiashanshuiItem()
        item['name'] = response.meta['name']
        item['img'] = response.meta['img']
        item['level'] = response.meta['level']
        item['province'] = response.xpath('//div[@class="media-right"]/ul/li[1]/span/text()').extract_first().split(' ')[1]
        item['location'] = response.xpath('//div[@class="media-right"]/ul/li[1]/span/text()').extract_first().split(' ')[2]
        item['opening'] = response.xpath('//div[@class="media-right"]/ul/li[@class="time"]/span/text()').extract_first()
        # print(response.text)
        html = response.text.replace('<br />', '***zch***')
        response_content = etree.HTML(html)
        content = response_content.xpath('//div[@class="produce_con"]')[0]
        text = content.xpath('string(.)').replace('\xa0', '').replace(' ', '').replace('\r', '')\
            .replace('\t', '').replace('***zch***', '\n').split('\n')
        item['content'] = [i for i in text if i != '']
        # print(dir(content))
        # item['content'] = content.getall()[0]
        yield item

