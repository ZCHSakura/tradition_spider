import csv

with open('../../xiehouyu_info.csv', 'a', encoding="utf-8", newline='') as file_obj:
    writer = csv.writer(file_obj)
    row = ["question", "answer"]
    writer.writerow(row)
