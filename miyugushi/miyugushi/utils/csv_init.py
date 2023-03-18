import csv

with open('../../miyugushi_info.csv', 'a', encoding="utf-8", newline='') as file_obj:
    writer = csv.writer(file_obj)
    row = ["name", "content", "annotation"]
    writer.writerow(row)
