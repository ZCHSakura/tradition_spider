# -*- coding: utf-8 -*-
import scrapy
import requests
from lxml import etree

from zuozhe.items import ZuozheItem


class AuthorSpider(scrapy.Spider):
    name = 'author'
    allowed_domains = ['so.gushiwen.org']
    start_urls = ['https://so.gushiwen.org/authors/Default.aspx?p=1&c=%e6%b8%85%e4%bb%a3']

    def parse(self, response):
        author_list = response.xpath('//div[@class="sonspic"]')
        for author in author_list:
            url = 'https://so.gushiwen.org/' + author.\
                xpath('.//a[@style="font-size:18px; line-height:22px; height:22px;"]/@href').extract_first()
            yield scrapy.Request(url, callback=self.author_info)

        # 翻页
        next_page = response.xpath('//a[@class="amore"]/@href').extract_first()
        if next_page:
            next_url = 'https://so.gushiwen.org' + next_page
            yield scrapy.Request(next_url, callback=self.parse)

    def author_info(self, response):
        item = ZuozheItem()
        item['info_1'] = None
        item['info_2'] = None
        item['info_3'] = None
        item['info_4'] = None
        item['info_5'] = None
        item['info_6'] = None
        item['info_7'] = None
        item['info_8'] = None
        item['info_9'] = None
        item['info_10'] = None
        item['info_11'] = None
        item['info_12'] = None
        item['info_13'] = None
        item['info_14'] = None
        item['info_15'] = None
        num = 0
        item['name'] = response.xpath('//h1[@style="height:22px; margin-bottom:10px;"]/span/b/text()').extract_first()
        item['img'] = response.xpath('//div[@class="divimg"]/img/@src').extract_first()
        intro = response.xpath('//div[@class="cont"]/p[@style=" margin:0px;"]')
        temp = intro[0].xpath('string(.)').extract_first()
        laji = response.xpath('//div[@class="cont"]/p[@style=" margin:0px;"]/a/text()').extract_first()
        if laji:
            item['intro'] = temp.replace(laji, '').replace('\n', '').replace(' ', '')
        else:
            item['intro'] = temp.replace('\n', '').replace(' ', '')
        if response.xpath('//div[@class="left"]//div[@class="title"]'):
            info_list = response.xpath('//div[@class="title"][1]/preceding-sibling::*[@class="sons" and '
                                   'not(@style="position:relative; z-index:0px;")]')
        else:
            info_list = response.xpath('//div[@class="sons" and not(@style="position:relative; z-index:0px;")]')
        for info in info_list:
            info_id = info.xpath('./@id').extract_first()
            if not info_id:
                # 没有下方信息的情况
                print('没有info_id')
                num += 1
                temp = info.xpath('./div[@class="contyishang"]')
                text = temp[0].xpath('string(.)').extract_first().split('\n')
                name = 'info_%s' % num
                item[name] = [i for i in text if i != '']
            else:
                info_id = info_id.replace('fanyiquan', '')
                num += 1
                r = requests.get('https://so.gushiwen.org/authors/ajaxziliao.aspx?id=%s' % info_id)
                html = str(r.text).replace('<br />', '\n')
                selector = etree.HTML(html)
                text = selector.xpath('//div[@class="contyishang"]')[0].xpath('string(.)').replace('▲', '').split('\n')
                name = 'info_%s' % num
                item[name] = [i for i in text if i != '']
        yield item
