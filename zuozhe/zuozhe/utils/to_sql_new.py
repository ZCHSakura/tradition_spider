# -*-coding:utf-8-*-

import csv
import ast
import pymysql

filename = "E:\\作业\\互联网+\\spider\\zuozhe\\author_info.csv"


with open(filename, 'r', encoding="utf-8") as f:
    reader = csv.reader(f)
    data = list(reader)
    data.pop(0)
    # print(type(data))

db = pymysql.connect('182.92.226.32', 'root', 'kybus123456', 'Chinese')
cursor = db.cursor()

for dd in data:
    dad = []
    # dad.extend([dd[0], dd[1], dd[2]])
    dad.extend([dd[0], dd[1], dd[2], str([ast.literal_eval(i) for i in dd[3:] if i != ''])])
    if dad[3] == '[]':
        dad[3] = None
    # print(dad[3])
    awsl = ['dsads','dsadsaaa','www','aaa']
    # print(awsl)
    xiaodidi = dd[:4]
    print(xiaodidi)
    # sql = "INSERT INTO tc_data_renwu(name,img,intro,information) VALUES ('%s','%s','%s','%s')" % (dad[0], dad[1], dad[2],awsl)
    sql = "INSERT INTO tc_data_renwu(name,img,intro,information) VALUES (%s,%s,%s,%s)"
    # print(sql)
    cursor.execute(sql, dad)
    db.commit()
    # break


# sql = "INSERT INTO author(name,img,intro,information) VALUES(%s,%s,%s,%s)"
# cursor.executemany(sql, datt)
#
print("数据库导入操作")

db.close




