import csv

with open('../../youerkepu.csv', 'a', encoding="utf-8", newline='') as file_obj:
    writer = csv.writer(file_obj)
    row = ["type", "name", "content"]
    writer.writerow(row)
