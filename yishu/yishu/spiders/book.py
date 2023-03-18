# -*- coding: utf-8 -*-
import scrapy

from yishu.items import YishuItem, ChapterItem


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['2345daohang.com']
    start_urls = ['https://www.2345daohang.com/zhongyi/']

    def parse(self, response):
        categorys = response.xpath('//ul[@class="re"]/li')
        for category in categorys:
            # 判断是不是有效的种类，最前面还有一个‘分类’
            if category.xpath('./a/@href').extract_first():
                categoryPage = 'https://www.2345daohang.com' + category.xpath('./a/@href').extract_first()
                request1 = scrapy.Request(categoryPage, callback=self.bookList)
                request1.meta['category'] = category.xpath('./a/text()').extract_first()
                yield request1

    def bookList(self, response):
        books = response.xpath('//ul[@class="asl"]/li')
        for book in books:
            if book.xpath('./a/@href').extract_first():
                bookPage = 'https://www.2345daohang.com' + book.xpath('./a/@href').extract_first()
                request2 = scrapy.Request(bookPage, callback=self.bookInfo)
                request2.meta['category'] = response.meta['category']
                request2.meta['name'] = book.xpath('./a/text()').extract_first()
                yield request2

        # 翻页
        next_page = response.xpath('//div[@class="page"]/a[contains(text(),"下一页")]/@href').extract_first()
        if next_page:
            next_url = 'https://www.2345daohang.com' + next_page
            yield scrapy.Request(next_url, callback=self.bookList, meta={'category': response.meta['category']})

    def bookInfo(self, response):
        item = YishuItem()
        item['category'] = response.meta['category']
        item['name'] = response.meta['name']

        if response.xpath('//div[@class="t"][1]/img/@src').extract_first():
            item['cover'] = 'https://www.2345daohang.com' + response.xpath('//div[@class="t"][1]/img/@src').extract_first()
        else:
            item['cover'] = None

        # author单独写：手册，教材
        if item['category'] == '教材':
            item['author'] = None
        if item['category'] == '手册':
            if response.xpath('//div[@class="t"]/h3[1][contains(text(),"着") '
                    'or contains(text(),"编") or contains(text(),"著")]'):
                item['author'] = response.xpath('//div[@class="t"]/h3[1][contains(text(),"着") '
                    'or contains(text(),"编") or contains(text(),"著")]/text()').extract_first()
            else:
                item['author'] = None
        else:
            item['author'] = response.xpath('//div[@class="t"][1]/div/a/text()').extract_first()
        # 没有intro:教材，手册，
        item['intro'] = response.xpath('//div[@class="t"][1]/p[1]/text()').extract_first().replace('\r\n', '')
        yield item

        yield scrapy.Request(response.url, callback=self.chapterList, meta={'bookName': item['name']}, dont_filter=True)


    def chapterList(self, response):
        bookName = response.meta['bookName']
        bookChapterList = response.xpath('//div[@class="t"][2]/h3[not(contains(text(),"着") '
                    'or contains(text(),"编") or contains(text(),"著"))]')
        chapterTitleNum = 0
        for bookChapter in bookChapterList:
            chapterTitleNum += 1
            # 如果这个章节标题本身不含有内容
            if bookChapter.xpath('./text()'):
                chapterTitle = bookChapter.xpath('./text()').extract_first()
                # 如果有细分chapterName,也就是细分章节
                if bookChapter.xpath('./following-sibling::ul[1]/li'):
                    chapterNameNum = 0
                    chapterNames = bookChapter.xpath('./following-sibling::ul[1]/li')
                    for chapterNamee in chapterNames:
                        chapterNameNum += 1
                        chapterName = chapterNamee.xpath('./a/text()').extract_first()
                        infoUrl = 'https://www.2345daohang.com' + chapterNamee.xpath('./a/@href').extract_first()
                        request3 = scrapy.Request(infoUrl, callback=self.chapterInfo)
                        request3.meta['bookName'] = bookName
                        request3.meta['chapterTitleNum'] = chapterTitleNum
                        request3.meta['chapterTitle'] = chapterTitle
                        request3.meta['chapterName'] = chapterName
                        request3.meta['chapterNameNum'] = chapterNameNum
                        request3.meta['haveContent'] = True
                        yield request3
                # 如果没有细分chapterName
                else:
                    item = ChapterItem()
                    item['bookName'] = bookName
                    item['chapterTitleNum'] = chapterTitleNum
                    item['chapterTitle'] = chapterTitle
                    item['chapterNameNum'] = 0
                    item['chapterName'] = None
                    item['haveContent'] = False
                    item['content'] = None
                    yield item
            # 如果这个章节标题本身含有内容
            elif bookChapter.xpath('./a/text()'):
                chapterTitle = bookChapter.xpath('./a/text()').extract_first()
                infoUrl = 'https://www.2345daohang.com' + bookChapter.xpath('./a/@href').extract_first()
                request4 = scrapy.Request(infoUrl, callback=self.chapterInfo)
                request4.meta['bookName'] = bookName
                request4.meta['chapterTitleNum'] = chapterTitleNum
                request4.meta['chapterTitle'] = chapterTitle
                request4.meta['chapterNameNum'] = 0
                request4.meta['chapterName'] = None
                request4.meta['haveContent'] = True
                yield request4
                # 如果有细分chapterName,也就是细分章节
                if bookChapter.xpath('./following-sibling::ul[1]/li'):
                    chapterNameNum = 0
                    chapterNames = bookChapter.xpath('./following-sibling::ul[1]/li')
                    for chapterNamee in chapterNames:
                        chapterNameNum += 1
                        chapterName = chapterNamee.xpath('./a/text()').extract_first()
                        infoUrl = 'https://www.2345daohang.com' + chapterNamee.xpath('./a/@href').extract_first()
                        request5 = scrapy.Request(infoUrl, callback=self.chapterInfo)
                        request5.meta['bookName'] = bookName
                        request5.meta['chapterTitleNum'] = chapterTitleNum
                        request5.meta['chapterTitle'] = chapterTitle
                        request5.meta['chapterName'] = chapterName
                        request5.meta['chapterNameNum'] = chapterNameNum
                        request5.meta['haveContent'] = True
                        yield request5
                # 如果没有细分chapterName则无操作，因为章节标题已在上方抛出

    def chapterInfo(self, response):
        item = ChapterItem()
        item['bookName'] = response.meta['bookName']
        item['chapterTitleNum'] = response.meta['chapterTitleNum']
        item['chapterTitle'] = response.meta['chapterTitle']
        item['chapterName'] = response.meta['chapterName']
        item['chapterNameNum'] = response.meta['chapterNameNum']
        item['haveContent'] = response.meta['haveContent']
        # todo 完成章节内容获取
        content = response.xpath('//div[@class="t"]/div')[0].xpath('string(.)').extract_first().replace(' ', '')\
            .replace('\t', '').split('\n')
        item['content'] = [i for i in content if i != '']
        yield item
