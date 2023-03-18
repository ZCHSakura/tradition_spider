# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv


class HuaxiashanshuiPipeline(object):
    def process_item(self, item, spider):
        with open('tourism_wenhuazongjiao_info.csv', 'a', encoding="utf-8", newline='') as file_obj:
            writer = csv.writer(file_obj)
            row = [item["name"], item["img"], item['level'], item['province'], item['location'], item['opening'], item['content']]
            writer.writerow(row)
