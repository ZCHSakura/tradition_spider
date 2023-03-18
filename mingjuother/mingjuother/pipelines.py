# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv


class MingjuotherPipeline(object):
    def process_item(self, item, spider):
        with open('mingju_other_info.csv', 'a', encoding="utf-8", newline='') as file_obj:
            writer = csv.writer(file_obj)
            row = [item["theme"], item["classify"], item['content'], item['come_from']]
            writer.writerow(row)
