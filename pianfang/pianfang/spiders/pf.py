# -*- coding: utf-8 -*-
import scrapy
from lxml import etree


from pianfang.items import PianfangItem


class PfSpider(scrapy.Spider):
    name = 'pf'
    allowed_domains = ['2345daohang.com']
    start_urls = ['https://www.2345daohang.com/pianfang/']

    def parse(self, response):
        pianfang_type_list = response.xpath('//div[@class="c"][2]/ul[@class="asl"]/li')
        for pianfang_type in pianfang_type_list:
            # 向内翻页
            info_page = pianfang_type.xpath('./a/@href').extract_first()
            if info_page:
                info_url = 'https://www.2345daohang.com' + info_page
                yield scrapy.Request(info_url, callback=self.pianfang_list_info)

    def pianfang_list_info(self, response):
        pianfang_list = response.xpath('//div[@class="c"][1]/ul[@class="asl"]/li')
        for pianfang in pianfang_list:
            name = pianfang.xpath('./a/text()').extract_first().replace('\r\n', '')
            # 向内翻页
            info_page = pianfang.xpath('./a/@href').extract_first()
            if info_page:
                info_url = 'https://www.2345daohang.com' + info_page
                request = scrapy.Request(info_url, callback=self.pianfang_info)
                request.meta['pianfang_type'] = response.xpath('//div[@id="nav"]/a[last()]/text()').extract_first()
                request.meta['name'] = name
                yield request

        # 向下翻页
        next_page = response.xpath('//a[contains(text(),"下一页")]/@href').extract_first()
        if next_page:
            next_url = 'https://www.2345daohang.com' + next_page
            yield scrapy.Request(next_url, callback=self.pianfang_list_info)

    def pianfang_info(self, response):
        item = PianfangItem()
        item['pianfang_type'] = response.meta['pianfang_type']
        item['name'] = response.meta['name']
        html = response.text.replace('<br>', '***zch***')
        response_content = etree.HTML(html)
        content = response_content.xpath('//div[@class="t"]/p')[0].xpath('string(.)').replace('\r\n', '').split('***zch***')
        item['content'] = [i for i in content if i != '']
        yield item
