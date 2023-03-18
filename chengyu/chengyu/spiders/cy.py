# -*- coding: utf-8 -*-
import scrapy

from chengyu.items import ChengyuItem


class CySpider(scrapy.Spider):
    name = 'cy'
    allowed_domains = ['2345daohang.com']
    start_urls = ['https://www.2345daohang.com/chengyu/list_1.htm']

    def parse(self, response):
        page = response.url.replace('https://www.2345daohang.com/chengyu/list_', '').replace('.htm', '')
        page = int(page) + 1
        name_list = response.xpath('//div[@class="c"][last()]/ul[@class="asl"]/li')
        for name in name_list:
            # 向内翻页
            info_page = name.xpath('./a/@href').extract_first()
            if info_page:
                info_url = 'https://www.2345daohang.com' + info_page
                yield scrapy.Request(info_url, callback=self.chengyu_info)

        # 向下翻页
        if int(page) < 312:
            next_url = 'https://www.2345daohang.com/chengyu/list_%s.htm' % page
            yield scrapy.Request(next_url, callback=self.parse)

    def chengyu_info(self, response):
        item = ChengyuItem()
        item['name'] = response.xpath('//div[@class="t"]/h3/text()').extract_first()\
            .replace('\r', '').replace('\n', '').replace('\t', '')
        item['pronunciation'] = response.xpath('///following-sibling::*/text()').extract_first()
        item['explanation'] = response.xpath('//em[contains(text(),"释义：")]/following-sibling::*/text()').extract_first()
        item['provenance'] = response.xpath('//em[contains(text(),"出自：")]/following-sibling::*/text()').extract_first()
        yield item
