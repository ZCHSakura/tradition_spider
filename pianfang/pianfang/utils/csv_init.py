import csv

with open('../../pianfang_info.csv', 'a', encoding="utf-8", newline='') as file_obj:
    writer = csv.writer(file_obj)
    row = ["pianfang_type", "name", "content"]
    writer.writerow(row)
