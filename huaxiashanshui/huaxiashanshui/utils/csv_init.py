import csv

with open('../../tourism_wenhuazongjiao_info.csv', 'a', encoding="utf-8", newline='') as file_obj:
    writer = csv.writer(file_obj)
    row = ["name", "img", "level", "province", "location", "opening", "content"]
    writer.writerow(row)