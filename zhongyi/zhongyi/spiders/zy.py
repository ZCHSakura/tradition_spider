# -*- coding: utf-8 -*-
import scrapy
from lxml import etree

from zhongyi.items import ZhongyiItem


class ZySpider(scrapy.Spider):
    name = 'zy'
    allowed_domains = ['2345daohang.com']
    start_urls = ['https://www.2345daohang.com/jiufang/list_1.htm']

    def parse(self, response):
        name_list = response.xpath('//div[@class="c"][1]/ul[@class="asl"]/li')
        for name in name_list:
            # 向内翻页
            info_page = name.xpath('./a/@href').extract_first()
            if info_page:
                info_url = 'https://www.2345daohang.com' + info_page
                yield scrapy.Request(info_url, callback=self.zhongyi_info)

        # 向下翻页
        next_page = response.xpath('//a[contains(text(),"下一页")]/@href').extract_first()
        if next_page:
            next_url = 'https://www.2345daohang.com' + next_page
            yield scrapy.Request(next_url, callback=self.parse)

    def zhongyi_info(self, response):
        html = response.text.replace('<br>', '***zch***')
        response_intro = etree.HTML(html)
        item = ZhongyiItem()
        item['theme'] = '酒方'
        item['name'] = response.xpath('//div[@class="t"]/h3/text()').extract_first().replace('\ufeff', '').replace('\r\n', '')
        intro = response_intro.xpath('//div[@class="t"]/p')[0].xpath('string(.)').replace('\r\n', '').split('***zch***')
        item['intro'] = [i for i in intro if i != '']
        yield item
