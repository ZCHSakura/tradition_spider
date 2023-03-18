# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv

from zhuanlan.items import yangshengItem, gongyiItem, minsuItem


def write_yangsheng_info(item):
    with open('yangsheng_info.csv', 'a', encoding="utf-8", newline='') as file_obj:
        writer = csv.writer(file_obj)
        row = [item["typeName"], item["name"], item['content']]
        writer.writerow(row)

def write_gongyi_info(item):
    with open('gongyi_info.csv', 'a', encoding="utf-8", newline='') as file_obj:
        writer = csv.writer(file_obj)
        row = [item["theme"], item["name"], item['cover'], item['author'], item['modifiedTime'], item['content']]
        writer.writerow(row)

def write_minsu_info(item):
    with open('minsu_info.csv', 'a', encoding="utf-8", newline='') as file_obj:
        writer = csv.writer(file_obj)
        row = [item["name"], item["author"], item['content']]
        writer.writerow(row)

class ZhuanlanPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, yangshengItem):
            write_yangsheng_info(item)
        if isinstance(item, gongyiItem):
            write_gongyi_info(item)
        if isinstance(item, minsuItem):
            write_minsu_info(item)
