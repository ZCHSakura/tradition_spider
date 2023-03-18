# -*-coding:utf-8-*-

import csv
import pymysql

db = pymysql.connect('182.92.226.32', 'root', 'kybus123456', 'theOld')
cursor = db.cursor()

sql1 = "SELECT id,bookName from main_data_gujizhangjie"
cursor.execute(sql1)  # 执行SQL语句
results = cursor.fetchall()  # 获取所有记录列表
i = 0
for result in results:
    i += 1
    print(i, result)
    id = result[0]
    bookName = result[1]
    sql2 = "SELECT id from main_data_jingdianguoxue where name = %s"
    cursor.execute(sql2, bookName)  # 执行SQL语句
    nn = cursor.fetchone()[0]  # 获取记录
    print(nn)
    sql3 = "UPDATE main_data_gujizhangjie SET bookId = %s where id = %s"
    data = []
    data.append(nn)
    data.append(id)
    try:
        # 执行SQL语句
        cursor.execute(sql3, data)
        # 提交修改
        db.commit()
    except:
        # 发生错误时回滚
        print('出错3')
        db.rollback()

db.close