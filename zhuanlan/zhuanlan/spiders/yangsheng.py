# -*- coding: utf-8 -*-
import scrapy
from lxml import etree

from zhuanlan.items import yangshengItem


class YangshengSpider(scrapy.Spider):
    name = 'yangsheng'
    allowed_domains = ['xuexila.com']
    start_urls = ['https://www.xuexila.com/yangsheng/yangshengzhishi/',
                  'https://www.xuexila.com/yangsheng/jiankangyinshi/']

    def parse(self, response):
        typeList = response.xpath('//div[@class="abox_list"]')
        for types in typeList:
            typeName = types.xpath('./h3/b/a/text()').extract_first()
            nextUrl = 'https:' + types.xpath('./h3/b/a/@href').extract_first()
            yield scrapy.Request(nextUrl, callback=self.infoList, meta={'typeName': typeName})

    def infoList(self, response):
        tipsList = response.xpath('//ul[@class="r_list"]/li')
        for tip in tipsList:
            name = tip.xpath('./h4/a/text()').extract_first()
            detailUrl = 'https:' + tip.xpath('./h4/a/@href').extract_first()
            yield scrapy.Request(detailUrl, callback=self.infoDetail, meta={'typeName': response.meta['typeName'], 'name': name})

    def infoDetail(self, response):
        item = yangshengItem()
        item['typeName'] = response.meta['typeName']
        item['name'] = response.meta['name']
        # 开始处理正文，主要是要去掉下面的推荐部分，scrapy的selector好像不能去掉部分子节点，所以我选择将html化为lxml的element
        # content = response.xpath('//div[@class="con_main"]')[0].xpath('string(.)').get().replace('\xa0', '') \
        #     .split('猜你喜欢')[0].split('\n')
        # item['content'] = [i for i in content if i != '']
        element = etree.HTML(response.text).xpath('//div[@class="con_main"]')[0]
        # 删除推荐的节点
        for pp in element.findall('p[@style]'):
            element.remove(pp)
        content = element.xpath('string(.)').replace('\xa0', '').replace('a("conten");', '').split('\n')
        item['content'] = [i for i in content if i != '']
        yield item
