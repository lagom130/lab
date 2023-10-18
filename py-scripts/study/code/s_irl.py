import csv
import json
import os


def no_title_csv_analysis(title, path):
    data_list = []

    with open(path, encoding='utf-8') as f:
        reader = csv.reader(f)
        for row_index, row in enumerate(reader):
            data = {}
            for index, i in enumerate(row):
                data[title[index]] = i
            data_list.append(data)

    return data_list



def sub_step(status):
    if status == 'unSend' :
        return 1
    elif status == 'finished':
        return 1
    else:
        return 0

def write_csv(data_list, path):
    with open(path, 'w', encoding='utf-8', newline='') as cf:
        writer = csv.writer(cf)
        for index, i in enumerate(data_list):
            for k in i.keys():
                if i[k] is None or i[k] is 'null':
                    i[k]: ''
            if index == 0:
                writer.writerow(i.keys())
            writer.writerow(i.values())


def write_txt(data_list, path):
    with open(path, 'w', encoding='utf-8', newline='') as cf:
        for item in data_list:
            cf.writelines(item)

if __name__ == '__main__':
    ir_original_status_list = no_title_csv_analysis(['id', 'info_resource_name', 'info_resource_life_cycle'],
                                                    "E:\\io816\\info_resource_816_life.csv")

    sql_list = []
    for ir in ir_original_status_list:
        sql_list.append(
            "UPDATE info_resource_platform set info_resource_life_cycle='" + ir['info_resource_life_cycle'] + "' where id ='"+ir['id']+"'; ")
    write_txt(sql_list, 'E:\\io816\\irs.txt')
    print('over')

