# -*- coding: utf-8 -*-
import scrapy

from hongsejingdian.items import HongsejingdianItem


class HonglvSpider(scrapy.Spider):
    name = 'honglv'
    allowed_domains = ['redtourism.com.cn']
    start_urls = ['http://www.redtourism.com.cn/col/col173/index.html']

    def parse(self, response):
        # jingqu_list = response.xpath('//div[@class="con_imgs"]/ul/li')
        province_list = response.xpath('//div[@class="shengfen margin_auto"]/div/table/tr/td')
        for province in province_list:
            province_url = 'http://www.redtourism.com.cn' + province.xpath('./a/@href').extract_first()
            yield scrapy.Request(province_url, callback=self.province_info)

    def province_info(self, response):
        province = response.xpath('//div[@class="bt bjjs_bt"]/h4/text()').extract_first()
        jingqu_url = 'http://www.redtourism.com.cn' + response.xpath(
            '//div[@class="con_imgs"]/ul/li[1]/a/@href').extract_first()
        name = response.xpath('//div[@class="con_imgs"]/ul/li[1]//div[@class="glmd_font"]/text()').extract_first()
        img = 'http://www.redtourism.com.cn' + response.xpath(
            '//div[@class="con_imgs"]/ul/li[1]/a/img/@src').extract_first()
        request = scrapy.Request(jingqu_url, callback=self.jingqu_info)
        request.meta['name'] = name
        request.meta['province'] = province
        request.meta['img'] = img
        yield request

    def jingqu_info(self, response):
        item = HongsejingdianItem()
        item['name'] = response.meta['name']
        item['province'] = response.meta['province']
        item['img'] = response.meta['img']
        item['imgList'] = []
        img_list = response.xpath('//div[@class="content_con jqtk"]/div[@class="con_imgs"]/ul/li')
        for imgs in img_list:
            item['imgList'].append('http://www.redtourism.com.cn'+imgs.xpath('./a/img/@src').extract_first())
        item['level'] = response.xpath('//li[@style="color: black;" and contains(text(), "景区级别")]/font/text()').extract_first()
        item['location'] = response.xpath('//div[@class="jqls"]//li[@style="color: black;width:300px;height: 35px;overflow: hidden;"]/@title').extract_first()
        item['phone'] = response.xpath('//div[@class="jqls"]//li[contains(text(), "联系电话")]/text()').extract_first().replace('联系电话：', '')
        item['content'] = response.xpath('//div[@class="container"]/div[@class="content_introduction"]//span/text()').extract_first()
        yield item

