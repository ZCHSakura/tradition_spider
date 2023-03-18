# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv


class ShaoerkepuPipeline(object):
    def process_item(self, item, spider):
        if len(item['content']) == 0:
            with open('empty.csv', 'a', encoding="utf-8", newline='') as file_obj:
                writer = csv.writer(file_obj)
                row = [item['type'], item['name'], item['url']]
                writer.writerow(row)
        else:
            with open('youerkepu.csv', 'a', encoding="utf-8", newline='') as file_obj:
                writer = csv.writer(file_obj)
                row = [item["type"], item["name"], item['content']]
                writer.writerow(row)
