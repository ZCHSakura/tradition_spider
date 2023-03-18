# -*-coding:utf-8-*-

import csv
import pymysql

filename = "E:\\作业\\互联网+\\spider\\hongsewenxue\\hongxue_chapter.csv"


with open(filename, 'r', encoding="utf-8") as f:
    reader = csv.reader(f)
    data = list(reader)
    data.pop(0)

db = pymysql.connect('182.92.226.32', 'root', 'kybus123456', 'Chinese')
cursor = db.cursor()

sql = "INSERT INTO tc_data_hongsewenxuezhangjie(bookName,chapterNum,chapterName,content) VALUES(%s,%s,%s,%s)"
cursor.executemany(sql, data)

print("数据库导入操作")

db.commit()
db.close



