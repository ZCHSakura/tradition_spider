import csv

# with open('../../yangsheng_info.csv', 'a', encoding="utf-8", newline='') as file_obj:
#     writer = csv.writer(file_obj)
#     row = ["typeName", "name", "content"]
#     writer.writerow(row)

# with open('../../gongyi_info.csv', 'a', encoding="utf-8", newline='') as file_obj:
#     writer = csv.writer(file_obj)
#     row = ["theme", "name", "cover", "author", "modifiedTime", "content"]
#     writer.writerow(row)

with open('../../minsu_info.csv', 'a', encoding="utf-8", newline='') as file_obj:
    writer = csv.writer(file_obj)
    row = ["name", "author", "content"]
    writer.writerow(row)
