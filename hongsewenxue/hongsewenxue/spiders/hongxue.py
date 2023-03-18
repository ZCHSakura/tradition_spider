# -*- coding: utf-8 -*-
import time

import scrapy

from hongsewenxue.items import HongsewenxueItem, ChapterItem


class HongxueSpider(scrapy.Spider):
    name = 'hongxue'
    allowed_domains = ['eywedu.org']
    start_urls = ['http://www.eywedu.org/hongse.htm']

    def parse(self, response):
        book_list = response.xpath('//div[@id="youli2"]/ul/li')
        for book in book_list:
            name = book.xpath('./a/text()').extract_first().split('-')[0]
            author = book.xpath('./a/text()').extract_first().split('-')[1]
            book_info_url = 'http://www.eywedu.org/' + book.xpath('./a/@href').extract_first()
            request = scrapy.Request(book_info_url, callback=self.book_info)
            request.meta['name'] = name
            request.meta['author'] = author
            time.sleep(1)
            yield request

    def book_info(self, response):
        item = HongsewenxueItem()
        item['name'] = response.meta['name']
        item['author'] = response.meta['author']
        item['img'] = response.url.replace('index.html', '')+response.xpath('//p[@align="center"]/img/@src').extract_first()
        yield item
        chapter_list = response.xpath('//div[@id="youli2"]/ul/li')
        for chapter in chapter_list:
            chapter_num = chapter.xpath('./a/@href').extract_first().replace('00', '').replace('.htm', '')
            chapter_name = chapter.xpath('./a/text()').extract_first()
            chapter_url = response.url.replace('index.html', '')+chapter.xpath('./a/@href').extract_first()
            request = scrapy.Request(chapter_url, callback=self.chapter_info)
            request.meta['chapter_num'] = chapter_num
            request.meta['chapter_name'] = chapter_name
            request.meta['book_name'] = response.meta['name']
            yield request

    def chapter_info(self, response):
        item = ChapterItem()
        item['book_name'] = response.meta['book_name']
        item['chapter_num'] = response.meta['chapter_num']
        item['chapter_name'] = response.meta['chapter_name']
        content = response.xpath('//div[@class="content"]/table/tr/td')[0].xpath('string(.)').extract_first().split('上一页回 目 录下一页\r\n')[0].split('\r\n')
        item['content'] = [i for i in content if i != '']
        yield item
