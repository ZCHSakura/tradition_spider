# -*- coding: utf-8 -*-
import scrapy

from mingju.items import MingjuItem


class MingjujuSpider(scrapy.Spider):
    name = 'mingjuju'
    allowed_domains = ['so.gushiwen.org']
    start_urls = ['https://so.gushiwen.org/guwen/default.aspx?p=1']

    def parse(self, response):
        book_list = response.xpath('//div[@class="sonspic"]')
        # book = book_list[10]
        for book in book_list:
            mingju_uurrll = book.xpath('.//a[contains(text(), "名句") and @target="_blank"]/@href').extract_first()
            if mingju_uurrll:
                mingju_url = 'https://so.gushiwen.org' + mingju_uurrll
                request = scrapy.Request(mingju_url, callback=self.mingju_list)
                book_name = book.xpath('.//p[@style="height:22px;"]//b/text()').extract_first()
                request.meta['book_name'] = book_name
                print(book_name)
                yield request

        # 翻页
        next_page = response.xpath('//a[@class="amore"]/@href').extract_first()
        if next_page:
            next_url = 'https://so.gushiwen.org' + next_page
            yield scrapy.Request(next_url, callback=self.parse)

    def mingju_list(self, response):
        mingjuju_list = response.xpath('//div[@class="sons" and @style=" padding-bottom:12px;"]/div[@class="cont"]')
        for mingju in mingjuju_list:
            book_from = mingju.xpath('.//a[@target="_blank" and @style=" float:left;"][2]/text()')\
                .extract_first().replace('《', '').replace('》', '').split('·')
            if len(book_from) == 3:
                chapter_title = book_from[1]
                chapter_name = book_from[2]
            elif len(book_from) == 2:
                chapter_title = None
                chapter_name = book_from[1]
            else:
                print('到底是哪里出了问题?')
                print(response.url)
            content = mingju.xpath('./a[@style=" float:left;"][1]/text()').extract_first()
            if content:
                print(response.url)
            mingju_url = 'https://so.gushiwen.org' + mingju.xpath\
                ('./a[@style=" float:left;"][1]/@href').extract_first()
            print(mingju_url)
            print(book_from)
            request = scrapy.Request(mingju_url, callback=self.mingju_info)
            request.meta['book_name'] = response.meta['book_name']
            request.meta['chapter_title'] = chapter_title
            request.meta['chapter_name'] = chapter_name
            request.meta['content'] = content
            yield request

    def mingju_info(self, response):
        item = MingjuItem()
        item['book_name'] = response.meta['book_name']
        item['chapter_title'] = response.meta['chapter_title']
        item['chapter_name'] = response.meta['chapter_name']
        item['content'] = response.meta['content']
        item['translation'] = response.xpath('//div[@class="contson"]/text()').extract_first().replace('\n', '')\
            .replace('解释：', '')
        yield item

