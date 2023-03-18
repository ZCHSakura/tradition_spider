# -*-coding:utf-8-*-

import MySQLdb

db = MySQLdb.connect('182.92.226.32', 'root', 'kybus123456', 'theOld', charset='utf8')
cursor = db.cursor(MySQLdb.cursors.DictCursor)

sql1 = "SELECT `id`,`bookName` FROM main_data_yishuzhangjie WHERE `bookId` IS NULL ORDER BY `id`"
cursor.execute(sql1)
results = cursor.fetchall()  # 获取所有记录
for row in results:
    id = row['id']
    bookName = row['bookName']
    sql2 = "SELECT `id` FROM main_data_zhongyiyangsheng WHERE name = %s"
    cursor.execute(sql2, [bookName])
    bookId = cursor.fetchone()['id']
    sql3 = "UPDATE main_data_yishuzhangjie SET `bookId` = %s WHERE `id` = %s"
    try:
        # 执行SQL语句
        cursor.execute(sql3, [bookId, id])
        # 提交修改
        db.commit()
        print(id)
    except:
        # 发生错误时回滚
        db.rollback()
        print(0)

db.close
