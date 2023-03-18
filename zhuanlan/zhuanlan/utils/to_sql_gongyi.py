# -*-coding:utf-8-*-

import csv
import pymysql

filename = "E:\\作业\\互联网+\\spider\\zhuanlan\\gongyi_info.csv"


with open(filename, 'r', encoding="utf-8") as f:
    reader = csv.reader(f)
    data = list(reader)
    data.pop(0)

db = pymysql.connect('182.92.226.32', 'root', 'kybus123456', 'theOld')
cursor = db.cursor()

i = 0
for dd in data:
    i += 1
    sql1 = "SELECT id from user_userInfo WHERE nickname = %s"
    if dd[3] == '':
        dd[3] = '官方1号'
    cursor.execute(sql1, dd[3])  # 执行SQL语句
    results = cursor.fetchall()  # 获取所有记录列表
    if results:
        sql2 = "INSERT INTO main_data_tougaolanmu(theme,name,cover,userId,modifiedTime,content) VALUES(%s,%s,%s,%s,%s,%s)"
        dad = dd
        dad[3] = results[0][0]
        try:
            # 执行SQL语句
            cursor.execute(sql2, dad)
            # 提交修改
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()
    else:
        sql3 = "INSERT INTO user_userInfo(nickname) VALUES(%s)"
        try:
            # 执行SQL语句
            cursor.execute(sql3, dd[3])
            # 提交修改
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()
        cursor.execute(sql1, dd[3])  # 执行SQL语句
        result = cursor.fetchall()  # 获取所有记录列表
        sql4 = "INSERT INTO main_data_tougaolanmu(theme,name,cover,userId,modifiedTime,content) VALUES(%s,%s,%s,%s,%s,%s)"
        dad = dd
        dad[3] = result[0][0]
        try:
            # 执行SQL语句
            cursor.execute(sql4, dad)
            # 提交修改
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()
    print(i, results)

db.close



