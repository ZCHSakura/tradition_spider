import csv

with open('../../yao_jiu_zhou_info.csv', 'a', encoding="utf-8", newline='') as file_obj:
    writer = csv.writer(file_obj)
    row = ["theme", "name", "intro"]
    writer.writerow(row)
