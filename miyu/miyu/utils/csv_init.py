import csv

with open('../../miyu_info.csv', 'a', encoding="utf-8", newline='') as file_obj:
    writer = csv.writer(file_obj)
    row = ["miyu_type", "question", "answer", "annotation"]
    writer.writerow(row)
