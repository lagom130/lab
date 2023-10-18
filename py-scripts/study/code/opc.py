import csv
import json


def csv_analysis_to_dict(path):
    dept_dict = {}

    with open(path, encoding='utf-8') as f:
        reader = csv.reader(f)
        for row_index, row in enumerate(reader):
            dept_dict[row[0]] = row[1]
    return dept_dict

def csv_analysis(path, dict):
    title = []
    data_list = []
    map_dict = {}

    with open(path, encoding='utf-8') as f:
        reader = csv.reader(f)
        for row_index, row in enumerate(reader):
            if row_index is 0:
                title = row

            else:
                data = {
                    'resource_name': row[0],
                    'dept': dict[row[1]]
                }
                data_list.append(data)
    return data_list


def str_to_hump(text):
    arr = filter(None, text.lower().split('_'))
    res = ''
    for index, i in enumerate(arr):
        f = i[0].lower()
        if index is not 0:
            f = f.upper()
        res = res + f+i[1:]
    return res

if __name__ == '__main__':
    org_department_dict = csv_analysis_to_dict("E:\\org_department.csv")
    data_list = csv_analysis("E:\\open.csv", org_department_dict)
    with open("E:\\3.csv", 'w', encoding='utf-8', newline='') as cf:
        writer = csv.writer(cf)
        for index, i in enumerate(data_list):
            for k in i.keys():
                if i[k] is None or i[k] is 'null':
                    i[k]: ''
            if index == 0:
                writer.writerow(i.keys())
            writer.writerow(i.values())
