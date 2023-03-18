import csv

with open('../../yanyu_info.csv', 'a', encoding="utf-8", newline='') as file_obj:
    writer = csv.writer(file_obj)
    row = ["yanyu_type", "content"]
    writer.writerow(row)
