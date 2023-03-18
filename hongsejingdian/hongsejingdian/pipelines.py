# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv


class HongsejingdianPipeline(object):
    def process_item(self, item, spider):
        with open('hongsejingdian_info.csv', 'a', encoding="utf-8", newline='') as file_obj:
            writer = csv.writer(file_obj)
            row = [item["name"], item["province"], item["img"], item["imgList"], item["level"], item["location"], item["phone"], item["content"]]
            writer.writerow(row)
