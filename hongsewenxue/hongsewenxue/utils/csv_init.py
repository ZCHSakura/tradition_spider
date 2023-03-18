import csv

with open('../../hongxue_chapter.csv', 'a', encoding="utf-8", newline='') as file_obj:
    writer = csv.writer(file_obj)
    row = ["book_name", "chapter_num", "chapter_name", "content"]
    writer.writerow(row)