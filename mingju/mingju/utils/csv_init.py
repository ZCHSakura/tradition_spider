import csv

with open('../../mingju_info.csv', 'a', encoding="utf-8", newline='') as file_obj:
    writer = csv.writer(file_obj)
    row = ["book_name", "chapter_title", "chapter_name", "content", "translation"]
    writer.writerow(row)
