# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv

from gushiwenwang.items import BookItem, ChapterItem

def write_book_info(item):
    with open('book_info.csv', 'a', encoding="utf-8", newline='') as file_obj:
        writer = csv.writer(file_obj)
        row = [item["name"], item["img"], item['intro']]
        writer.writerow(row)


def write_chapter_info(item):
    with open('chapter_info.csv', 'a', encoding="utf-8", newline='') as file_obj:
        writer = csv.writer(file_obj)
        row = [item["book_name"], item["chapter_title"], item['chapter_name'], item['content'], item['translation'], item['annotation'], item['note']]
        writer.writerow(row)


class GushiwenwangPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, BookItem):
            write_book_info(item)
        if isinstance(item, ChapterItem):
            write_chapter_info(item)
