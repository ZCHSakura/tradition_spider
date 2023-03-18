import csv

with open('../../author_info.csv', 'a', encoding="utf-8", newline='') as file_obj:
    writer = csv.writer(file_obj)
    row = ["name", "img", "intro", "info_1", "info_2", "info_3", "info_4", "info_5", "info_6", "info_7", "info_8",
           "info_9", "info_10", "info_11", "info_12", "info_13", "info_14", "info_15"]
    writer.writerow(row)
