# -*- coding: utf-8 -*-
import scrapy
from lxml import etree


from zhougongjiemeng.items import ZhougongjiemengItem


class ZgjmSpider(scrapy.Spider):
    name = 'zgjm'
    allowed_domains = ['2345daohang.com']
    start_urls = ['https://www.2345daohang.com/zgjm/list_11.htm']

    def parse(self, response):
        dream_type = response.xpath('//div[@class="r1"]/text()').extract_first()
        dream_list = response.xpath('//div[@class="c"]/ul/li')
        for dream in dream_list:
            theme = dream.xpath('./a/text()').extract_first()
            if response.url == 'https://www.2345daohang.com/zgjm/list_11.htm':
                theme = dream.xpath('./a/text()').extract_first().replace('\r\n\r\n', '')
            # 向内翻页
            info_page = dream.xpath('./a/@href').extract_first()
            if info_page:
                info_url = 'https://www.2345daohang.com' + info_page
                request = scrapy.Request(info_url, callback=self.dream_info)
                request.meta['dream_type'] = dream_type
                request.meta['theme'] = theme
                # 只有第十一页需要这个，请注意
                request.meta['biaozhi'] = True
                yield request

        # 向下翻页
        next_page = response.xpath('//a[contains(text(),"下一页")]/@href').extract_first()
        if next_page:
            next_url = 'https://www.2345daohang.com' + next_page
            yield scrapy.Request(next_url, callback=self.parse)

    def dream_info(self, response):
        item = ZhougongjiemengItem()
        item['dream_type'] = response.meta['dream_type']
        item['theme'] = response.meta['theme']
        if not response.meta['biaozhi']:
            text = response.xpath('//div[@class="t"]/p')
            content = text[0].xpath('string(.)').extract_first().replace(' ', '').split('\r\n')
            item['content'] = [i for i in content if i != '']
            yield item
        if response.meta['biaozhi']:
            item['theme'] = item['theme'].replace('\r\n\r\n', '')
            html = response.text.replace('<br>', '***zch***')
            response11 = etree.HTML(html)
            text = response11.xpath('//div[@class="t"]/p')
            # print(text[0].xpath('string(.)').replace(' ', '').replace('\t', '').replace('\r\n', ''))
            content = text[0].xpath('string(.)').replace(' ', '').replace('\t', '').replace('\r\n', '')\
                .split('***zch***')
            item['content'] = [i for i in content if i != '']
            yield item

