import csv

with open('../../hongsejingdian_info.csv', 'a', encoding="utf-8", newline='') as file_obj:
    writer = csv.writer(file_obj)
    row = ["name", "province", "img", "imgList", "level", "location", "phone", "content"]
    writer.writerow(row)
