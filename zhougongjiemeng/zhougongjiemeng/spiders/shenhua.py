# -*- coding: utf-8 -*-
import scrapy


class ShenhuaSpider(scrapy.Spider):
    name = 'shenhua'
    allowed_domains = ['gs5000.cn']
    start_urls = ['http://gs5000.cn/']

    def parse(self, response):
        pass
