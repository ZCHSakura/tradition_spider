import csv

with open('../../shenhua.csv', 'a', encoding="utf-8", newline='') as file_obj:
    writer = csv.writer(file_obj)
    row = ["name", "img", "content"]
    writer.writerow(row)