# -*-coding:utf-8-*-

import ast
import csv
import pymysql

filename = "E:\\作业\\互联网+\\spider\\zuozhe\\author_info.csv"


with open(filename, 'r', encoding="utf-8") as f:
    reader = csv.reader(f)
    data = list(reader)
    data.pop(0)


# 17
# print(''.join(data[0][3:]))
a = ["\n".join(ast.literal_eval(i)) for i in data[0][3:] if i != '']
print(str(a))
print(type(a[0]))
print(a[0])
# ad = ast.literal_eval(a)
# print(type(a))
# print(type(a[0]))
#
# print(data[0][3:])
# print(type(data[0][3:]))
#
# print(data[0][3])
# ad = ast.literal_eval(data[0][3])
# print("\n".join(ad))

# for dd in data:
#     dad = []
#     dad.extend([dd[0], dd[1], dd[2], [i for i in dd[3:] if i != '']])
#     # dad[0] = dd[0]
#     # dad[1] = dd[1]
#     # dad[2] = dd[2]
#     # dad[3] = [i for i in dd[3:] if i != '']
#     print(dad[3][0])
