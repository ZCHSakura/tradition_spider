import csv

with open('../../book_info.csv', 'a', encoding="utf-8", newline='') as file_obj:
    writer = csv.writer(file_obj)
    row = ["category", "name", "cover", "author", "intro"]
    writer.writerow(row)

with open('../../chapter_info.csv', 'a', encoding="utf-8", newline='') as file_obj:
    writer = csv.writer(file_obj)
    row = ["bookName", "chapterTitleNum", "chapterTitle", "chapterNameNum", "chapterName", "haveContent", "content"]
    writer.writerow(row)
