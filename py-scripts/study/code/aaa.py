import csv
import json



def csv_analysis(path):
    title = []
    data_list = []

    with open(path, encoding='utf-8') as f:
        reader = csv.reader(f)
        for row_index, row in enumerate(reader):
            if row_index is 0:
                title = row

            else:
                data = {}
                for index, i in enumerate(row):
                    data[title[index]] = i
                data_list.append(data)
    return data_list



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

if __name__ == '__main__':
    resource_id_list = no_title_csv_analysis(['inf_resource_id','b','c'], "E:\\io816\\info_resource_816_life.csv")
    rids = []
    for row_index, row in enumerate(resource_id_list):
        rids.append(row['inf_resource_id'])

    rids_str = "','".join(rids)
    print("SELECT * from info_resource_platform where id in('"+rids_str+"')")

