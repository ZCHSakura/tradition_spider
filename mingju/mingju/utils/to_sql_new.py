# -*-coding:utf-8-*-

import csv
import pymysql

filename = "E:\\作业\\互联网+\\spider\\mingju\\mingju_info.csv"


with open(filename, 'r', encoding="utf-8") as f:
    reader = csv.reader(f)
    data = list(reader)
    data.pop(0)

db = pymysql.connect('182.92.226.32', 'root', 'kybus123456', 'Chinese')
cursor = db.cursor()

for dd in data:
    dad = []
    if dd[1]:
        dd1 = dd[1]+'-'+dd[2]
    else:
        dd1 = dd[2]
    dad.extend([dd[0], dd1, dd[3], dd[4]])
    sql = "INSERT INTO tc_data_qitamingju(classify,provenance,name,content) VALUES(%s,%s,%s,%s)"
    # print(dad)
    cursor.execute(sql, dad)
    db.commit()

# sql = "INSERT INTO tc_data_gujimingju(book_name,chapter_title,chapter_name,content, translation) VALUES(%s,%s,%s,%s,%s)"
# cursor.executemany(sql, data)

print("数据库导入操作")

db.close



