import csv

with open('../../shuhua_info_new.csv', 'a', encoding="utf-8", newline='') as file_obj:
    writer = csv.writer(file_obj)
    row = ["name", "img", "content_url", "content", "dynasty", "author", "size", "pixel", "intro"]
    writer.writerow(row)
