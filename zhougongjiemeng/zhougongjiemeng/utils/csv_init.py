import csv

with open('../../zhougongjiemeng_info.csv', 'a', encoding="utf-8", newline='') as file_obj:
    writer = csv.writer(file_obj)
    row = ["dream_type", "theme", "content"]
    writer.writerow(row)
