# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv

from yishu.items import YishuItem, ChapterItem


def write_book_info(item):
    with open('book_info.csv', 'a', encoding="utf-8", newline='') as file_obj:
        writer = csv.writer(file_obj)
        row = [item["category"], item["name"], item['cover'], item['author'], item['intro']]
        writer.writerow(row)

def write_chapter_info(item):
    with open('chapter_info.csv', 'a', encoding="utf-8", newline='') as file_obj:
        writer = csv.writer(file_obj)
        row = [item["bookName"], item["chapterTitleNum"], item['chapterTitle'], item['chapterNameNum'], item['chapterName'], item['haveContent'], item['content']]
        writer.writerow(row)

class YishuPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, YishuItem):
            write_book_info(item)
        if isinstance(item, ChapterItem):
            write_chapter_info(item)
