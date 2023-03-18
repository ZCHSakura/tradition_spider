# -*-coding:utf-8-*-

import csv
import pymysql

filename = "E:\\作业\\互联网+\\spider\\zhenbaoguan\\shuhua_info_new.csv"

with open(filename, 'r', encoding="utf-8") as f:
    reader = csv.reader(f)
    data = list(reader)
    data.pop(0)

db = pymysql.connect('59.110.223.221', 'root', 'zch621', 'tietouwa')
cursor = db.cursor()

sql = "INSERT INTO homepage(name, img, content_url, content, dynasty, author, size, pixel, intro) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
cursor.executemany(sql, data)

print("数据库导入操作")

db.commit()
db.close