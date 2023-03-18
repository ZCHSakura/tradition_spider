import csv

with open('../../chengyu_info.csv', 'a', encoding="utf-8", newline='') as file_obj:
    writer = csv.writer(file_obj)
    row = ["name", "pronunciation", "explanation", "provenance"]
    writer.writerow(row)
