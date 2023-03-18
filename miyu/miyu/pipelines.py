# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv


class MiyuPipeline(object):
    def process_item(self, item, spider):
        with open('miyu_info.csv', 'a', encoding="utf-8", newline='') as file_obj:
            writer = csv.writer(file_obj)
            row = [item["miyu_type"], item["question"], item["answer"], item["annotation"]]
            writer.writerow(row)
