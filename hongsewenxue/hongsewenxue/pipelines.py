# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv

from hongsewenxue.items import HongsewenxueItem, ChapterItem


def write_book_info(item):
    with open('hongxue_book.csv', 'a', encoding="utf-8", newline='') as file_obj:
        writer = csv.writer(file_obj)
        row = [item["name"], item["author"], item['img']]
        writer.writerow(row)


def write_chapter_info(item):
    with open('hongxue_chapter.csv', 'a', encoding="utf-8", newline='') as file_obj:
        writer = csv.writer(file_obj)
        row = [item["book_name"], item["chapter_num"], item['chapter_name'], item['content']]
        writer.writerow(row)

class HongsewenxuePipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, HongsewenxueItem):
            write_book_info(item)
        if isinstance(item, ChapterItem):
            write_chapter_info(item)
