# -*- coding: utf-8 -*-
import csv

import scrapy
import requests
from lxml import etree

from gushiwenwang.items import BookItem, ChapterItem

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/8'
                         '0.0.3987.106 Safari/537.36',
           'cookie': 'login=flase; gsw2017user=676029%7c02C683435F3F3863066DF52EC3F42B18; '
                     'login=flase; gswZhanghao=13572761631; gswPhone=13572761631; '
                     'Hm_lvt_04660099568f561a75456483228a9516=1581755001,1581841834,1581855332,1581918608; '
                     'sec_tc=AQAAACY0wD3S+AAAd3vNmZMrKLqdLE8U; ASP.NET_SessionId=m11qou4n0dqcnney4n31m5rh; '
                     'Hm_lpvt_04660099568f561a75456483228a9516=1581940956',
           'referer': '',
           'accept': '*/*',
           'accept-encoding': 'gzip, deflate, br',
           'accept-language': 'zh-CN,zh;q=0.9',
           'cache-control': 'no-cache',
           'pragma': 'no-cache',
           'sec - fetch - dest': 'empty',
           'sec - fetch - mode': 'cors',
           'sec - fetch - site': 'same - origin'}

class GujiSpider(scrapy.Spider):
    name = 'guji'
    allowed_domains = ['so.gushiwen.org']
    start_urls = ['https://so.gushiwen.org/guwen/Default.aspx?p=37']

    def parse(self, response):
        book_list = response.xpath('//div[@class="sonspic"]')
        # book = book_list[10]
        for book in book_list:
            # print(book.text)
            book_url = 'https://so.gushiwen.org' + book.xpath(
                './div[@class="cont"]/p[@style="height:22px;"]/a[@target="_blank"]/@href').extract_first()
            request = scrapy.Request(book_url, callback=self.book_info)
            intro = book.xpath('./div[@class="cont"]/p[@style=" margin:0px;"]')
            temp = intro[0].xpath('string(.)').extract_first()
            laji = book.xpath('./div[@class="cont"]/p[@style=" margin:0px;"]/a/text()').extract_first()
            if laji:
                request.meta['intro'] = temp.replace(laji, '').replace('\n', '').replace(' ', '')
            else:
                request.meta['intro'] = temp.replace('\n', '').replace(' ', '')
            yield request

        # 翻页
        # next_page = response.xpath('//a[@class="amore"]/@href').extract_first()
        # if next_page:
        #     next_url = 'https://so.gushiwen.org' + next_page
        #     yield scrapy.Request(next_url, callback=self.parse)

    def book_info(self, response):
        item = BookItem()
        item['name'] = response.xpath('//span[@style="font-size:20px; line-height:22px; height:22px;"]/b/text()')\
            .extract_first()
        item['img'] = response.xpath('//div[@class="divimg"]/img/@src').extract_first()
        item['intro'] = response.meta['intro']
        yield item
        chapter_list = response.xpath('//div[@class="bookcont"]/ul/span')
        if chapter_list:
            # 这种类别下不分章节标题，只有章节名称
            chapter_title = None
            # print(chapter_title)
            for chapter in chapter_list:
                chapter_name = chapter.xpath('./a/text()').extract_first()
                # print('---'+chapter_name+'---'+chapter_url)
                try:
                    chapter_url = 'https://so.gushiwen.org' + chapter.xpath('./a/@href').extract_first()
                    request = scrapy.Request(chapter_url, callback=self.chapter_info)
                    request.meta['book_name'] = item['name']
                    request.meta['chapter_title'] = chapter_title
                    request.meta['chapter_name'] = chapter_name
                    yield request
                except:
                    chapteritem = ChapterItem()
                    chapteritem['book_name'] = item['name']
                    chapteritem['chapter_title'] = chapter_title
                    chapteritem['chapter_name'] = chapter_name
                    chapteritem['content'] = None
                    chapteritem['translation'] = None
                    chapteritem['annotation'] = None
                    chapteritem['note'] = None
                    yield chapteritem
        else:
            chapter_title_list = response.xpath('//div[@class="bookcont"]')
            for chapter in chapter_title_list:
                # 章节标题
                chapter_title = chapter.xpath('./div[@class="bookMl"]/strong/text()').extract_first()
                # print(chapter_title)
                chapter_name_list = chapter.xpath('./div[@style=" clear:both; overflow:hidden; height:auto;"]/span')
                for cnl in chapter_name_list:
                    # 章节名称
                    chapter_name = cnl.xpath('./a/text()').extract_first()
                    try:
                        chapter_url = 'https://so.gushiwen.org' + cnl.xpath('./a/@href').extract_first()
                        request2 = scrapy.Request(chapter_url, callback=self.chapter_info)
                        request2.meta['book_name'] = item['name']
                        request2.meta['chapter_title'] = chapter_title
                        request2.meta['chapter_name'] = chapter_name
                        yield request2
                        # print('---'+chapter_name)
                    except:
                        chapteritem = ChapterItem()
                        chapteritem['book_name'] = item['name']
                        chapteritem['chapter_title'] = chapter_title
                        chapteritem['chapter_name'] = chapter_name
                        chapteritem['content'] = None
                        chapteritem['translation'] = None
                        chapteritem['annotation'] = None
                        chapteritem['note'] = None
                        yield chapteritem

    def chapter_info(self, response):
        item = ChapterItem()
        item['book_name'] = response.meta['book_name']
        item['chapter_title'] = response.meta['chapter_title']
        item['chapter_name'] = response.meta['chapter_name']
        # print(item['book_name']+'--'+str(item['chapter_title'])+'--'+item['chapter_name'])
        content = response.xpath('//div[@class="contson"]')
        item['content'] = content[0].xpath('string(.)').extract_first().replace(' ', '').split('\n')
        if item['content'][0] == '':
            del item['content'][0]
        if item['content'][-1] == '':
            del item['content'][-1]
        # print(item['content'])
        # 开始获取异步请求的译文和注释
        cid = response.xpath('//div[@class="left"][1]/@id').extract_first()
        if not cid:
            item['translation'] = None
            item['annotation'] = None
            item['note'] = None
            # 没有翻译的情况
            print('没有cid')
            print(item['book_name']+'--'+str(item['chapter_title'])+'--'+item['chapter_name'])
            return item
        else:
            cid = cid.replace('left', '')
        headers['referer'] = response.url
        r = requests.get('https://so.gushiwen.org/guwen/ajaxbfanyi.aspx?id=%s' % cid)
        # print(r.text)
        html = str(r.text).replace('<br />', '\n')
        # print(html)
        selector = etree.HTML(html)
        # 这不是值传递，我佛了
        selector_annotation = etree.HTML(html)
        print('https://so.gushiwen.org/guwen/ajaxbfanyi.aspx?id=%s' % cid)
        if selector:
            # 获取它到底是怎么个注释
            have_annotation = selector.xpath('//div[@class="shisoncont"]/h2//b/text()')[0]
            print('**'+have_annotation+'**')
            if have_annotation == '译文':
                # 这里和scrapy的response有所不同，要注意!!!
                translation = selector.xpath('//div[@class="shisoncont"]')[0]
                item['translation'] = translation.xpath('string(.)').replace('\n\n\n', '').replace('\n\n', '')\
                    .replace(' ', '').replace('全屏', '').replace('译文', '').split('\n')
                if item['translation'][0] == '':
                    del item['translation'][0]
                if item['translation'][-1] == '':
                    del item['translation'][-1]
                # print(item['translation'])
                item['annotation'] = None
                item['note'] = None
                yield item
            elif have_annotation == '译文及注释':
                translation = selector.xpath('//div[@class="shisoncont"]')[0]
                translation.remove(translation.getchildren()[-1])
                item['translation'] = translation.xpath('string(.)').replace('\n\n\n', '').replace('\n\n', '')\
                    .replace(' ', '').replace('译文及注释', '').replace('译文', '').replace('全屏', '').split('\n')
                if item['translation'][0] == '':
                    del item['translation'][0]
                if item['translation'][-1] == '':
                    del item['translation'][-1]
                annotation = selector_annotation.xpath('//div[@class="shisoncont"]/p[last()]')[0]
                # 这种方式，如果第一条注释和<strong>之间没有<br>的话，会导致第一条注释跟随<strong>一起被删除
                # annotation.remove(annotation.getchildren()[0])
                # TODO 完成对<br>的换行
                item['annotation'] = annotation.xpath('string(.)').replace('\n\n\n', '').replace('\n\n', '') \
                    .replace(' ', '').replace('全屏', '').replace('注释', '').split('\n')
                if item['annotation'][0] == '':
                    del item['annotation'][0]
                if item['annotation'][-1] == '':
                    del item['annotation'][-1]
                item['note'] = None
                # print('译文:'+item['translation'])
                # print('注释:'+item['annotation'])
                yield item
            elif have_annotation == '按语':
                note = selector.xpath('//div[@class="shisoncont"]')[0]
                item['note'] = note.xpath('string(.)').replace('\n\n\n', '').replace('\n\n', '') \
                    .replace(' ', '').replace('全屏', '').replace('按语', '').split('\n')
                if item['note'][0] == '':
                    del item['note'][0]
                if item['note'][-1] == '':
                    del item['note'][-1]
                item['translation'] = None
                item['annotation'] = None
                # print('按语:' + item['note'])
                yield item
            elif have_annotation == '注释及按语':
                note = selector.xpath('//div[@class="shisoncont"]/p[last()]')[0]
                item['note'] = note.xpath('string(.)').replace('\n\n\n', '').replace('\n\n', '') \
                    .replace(' ', '').replace('注释', '').split('\n')
                if item['note'][0] == '':
                    del item['note'][0]
                if item['note'][-1] == '':
                    del item['note'][-1]
                annotation = selector_annotation.xpath('//div[@class="shisoncont"]')[0]
                annotation.remove(annotation.getchildren()[-1])
                item['annotation'] = annotation.xpath('string(.)').replace('\n\n\n', '').replace('\n\n', '') \
                    .replace(' ', '').replace('全屏', '').replace('注释及按语', '').replace('按语', '').split('\n')
                if item['annotation'][0] == '':
                    del item['annotation'][0]
                if item['annotation'][-1] == '':
                    del item['annotation'][-1]
                item['translation'] = None
                # print('注释:' + item['annotation'])
                # print('按语:' + item['note'])
                yield item
            elif have_annotation == '段译':
                # TODO br换行
                translation = selector.xpath('//div[@class="shisoncont"]')[0]
                item['translation'] = translation.xpath('string(.)').replace('\n\n\n', '').replace('\n\n', '') \
                    .replace(' ', '').replace('全屏', '').replace('段译', '').split('\n')
                if item['translation'][0] == '':
                    del item['translation'][0]
                if item['translation'][-1] == '':
                    del item['translation'][-1]
                # print('段译:')
                # print(item['translation'])
                item['annotation'] = None
                item['note'] = None
                yield item
            elif have_annotation == '注释':
                # TODO br换行
                annotation = selector_annotation.xpath('//div[@class="shisoncont"]')[0]
                item['annotation'] = annotation.xpath('string(.)').replace('\n\n\n', '').replace('\n\n', '') \
                    .replace(' ', '').replace('全屏', '').replace('注释', '').split('\n')
                if item['annotation'][0] == '':
                    del item['annotation'][0]
                if item['annotation'][-1] == '':
                    del item['annotation'][-1]
                # print('注释:'+item['annotation'])
                item['translation'] = None
                item['note'] = None
                yield item
            # scar biss
            else:
                print('我是其他的')
                print(item['book_name'] + '--' + str(item['chapter_title']) + '--' + item['chapter_name'])
                print(response.url)
                item['translation'] = None
                item['annotation'] = None
        else:
            item['translation'] = None
            item['annotation'] = None
            item['note'] = None
            # 没有翻译的情况
            yield item
            print('没有得到翻译页面')
            print(item['book_name'] + '---' + str(item['chapter_title']) + '---' + item['chapter_name'])
            uurrll = 'https://so.gushiwen.org/guwen/ajaxbfanyi.aspx?id=%s' % cid
            print(uurrll)
            with open('have_no_translation.csv', 'a', encoding="utf-8", newline='') as file_obj:
                writer = csv.writer(file_obj)
                row = [uurrll]
                writer.writerow(row)
