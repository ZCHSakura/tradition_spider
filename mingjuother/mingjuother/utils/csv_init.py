import csv

with open('../../mingju_other_info.csv', 'a', encoding="utf-8", newline='') as file_obj:
    writer = csv.writer(file_obj)
    row = ["theme", "classify", "content", "come_from"]
    writer.writerow(row)
