# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv


class ZuozhePipeline(object):
    def process_item(self, item, spider):
        with open('author_info.csv', 'a', encoding="utf-8", newline='') as file_obj:
            writer = csv.writer(file_obj)
            row = [item["name"], item["img"], item["intro"], item["info_1"], item["info_2"], item["info_3"]
                , item["info_4"], item["info_5"], item["info_6"], item["info_7"], item["info_8"], item["info_9"]
                , item["info_10"], item["info_11"], item["info_12"], item["info_13"], item["info_14"], item["info_15"]]
            writer.writerow(row)
