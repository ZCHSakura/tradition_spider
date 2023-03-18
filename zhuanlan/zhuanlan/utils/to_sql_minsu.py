# -*-coding:utf-8-*-

import csv
import pymysql

filename = "E:\\作业\\互联网+\\spider\\zhuanlan\\minsu_info.csv"


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
    if dd[1] == '佚名':
        dd[1] = '官方2号'
    cursor.execute(sql1, dd[1])  # 执行SQL语句
    results = cursor.fetchall()  # 获取所有记录列表
    if results:
        sql2 = "INSERT INTO main_data_tougaolanmu(secondTypeId,name,userId,content,modifiedTime) VALUES(38,%s,%s,%s,NOW())"
        dad = dd
        dad[1] = results[0][0]
        try:
            # 执行SQL语句
            cursor.execute(sql2, dad)
            # 提交修改
            db.commit()
        except:
            # 发生错误时回滚
            print('出错1')
            db.rollback()
    else:
        sql3 = "INSERT INTO user_userInfo(nickname) VALUES(%s)"
        try:
            # 执行SQL语句
            cursor.execute(sql3, dd[1])
            # 提交修改
            db.commit()
        except:
            # 发生错误时回滚
            print('出错2')
            db.rollback()
        cursor.execute(sql1, dd[1])  # 执行SQL语句
        result = cursor.fetchall()  # 获取所有记录列表
        sql4 = "INSERT INTO main_data_tougaolanmu(secondTypeId,name,userId,content,modifiedTime) VALUES(38,%s,%s,%s,NOW())"
        dad = dd
        dad[1] = result[0][0]
        try:
            # 执行SQL语句
            cursor.execute(sql4, dad)
            # 提交修改
            db.commit()
        except:
            print('出错3')
            # 发生错误时回滚
            db.rollback()
    print(i, results)

db.close
