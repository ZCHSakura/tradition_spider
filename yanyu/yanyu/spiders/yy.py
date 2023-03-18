# -*- coding: utf-8 -*-
import scrapy

from yanyu.items import YanyuItem


class YySpider(scrapy.Spider):
    name = 'yy'
    allowed_domains = ['2345daohang.com']
    start_urls = ['https://www.2345daohang.com/yanyu/']

    def parse(self, response):
        type_list = response.xpath('//ul[@class="asl"]/li')
        for ttype in type_list:
            info_url = ttype.xpath('./a/@href').extract_first()
            if info_url:
                next_url = 'https://www.2345daohang.com' + info_url
                yield scrapy.Request(next_url, callback=self.yanyu_info)

    def yanyu_info(self, response):
        item = YanyuItem()
        item['yanyu_type'] = response.xpath('//div[@class="r1"]/text()').extract_first()
        yanyu_list = response.xpath('//ul[@class="asl"]/p')
        for yanyu in yanyu_list:
            item['content'] = yanyu.xpath('./text()').extract_first().replace('    ', '').replace('鈥檛', '\'t')\
                .replace('鈥檚', '\'s').replace('鈥橝', '\'A').replace('鈥?', '\' ')
            # print(item)
            yield item
