# -*-coding:utf-8-*-

import csv
import pymysql

filename = "E:\\作业\\互联网+\\spider\\zuozhe\\author_info.csv"


with open(filename, 'r', encoding="utf-8") as f:
    reader = csv.reader(f)
    data = list(reader)
    data.pop(0)

db = pymysql.connect('182.92.226.32', 'root', 'kybus123456', 'SpiderData')
cursor = db.cursor()

sql = "INSERT INTO tc_data_renwu(name,img,intro,info_1,info_2,info_3,info_4,info_5,info_6,info_7,info_8,info_9,info_10,info_11,info_12,info_13,info_14,info_15) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
cursor.executemany(sql, data)

print("数据库导入操作")

db.commit()
db.close



