import csv
import json
import os
import csv
import time


status_dict = {"cancel":"省级已撤销","published": "省级已上报"}
life_cycle_dict = {
    "0": "已创建",
    "1": "发布待审核",
    "2": "发布已驳回",
    "3": "已发布",
    "4": "撤销待审核",
    "5": "撤销已驳回",
    "6": "已撤销",
    "7": "已删除",
}



def csv_analysis_to_dict_list(path):
    dept_dict_list = []
    with open(path, encoding='utf-8') as f:
        reader = csv.reader(f)
        title = []
        for row_index, row in enumerate(reader):
            if row_index == 0:
                title = row
            else:
                item = {}
                for title_index, title_val in enumerate(title):
                    item[title_val] = row[title_index]
                dept_dict_list.append(item)
    return dept_dict_list

def csv_analysis_to_dict(path, key_name, value_name = None):
    dept_dict = {}
    title = []
    with open(path, encoding='utf-8') as f:
        reader = csv.reader(f)
        for row_index, row in enumerate(reader):
            if row_index == 0:
                title = row
            else:
                item = {}
                for title_index, title_val in enumerate(title):
                    item[title_val] = row[title_index]
                if value_name is None:
                    dept_dict[item[key_name]] = item
                else:
                    dept_dict[item[key_name]] = item[value_name]
    return dept_dict



def json_analysis_to_dict(path):
    json_fp = open(path, "r", encoding='utf-8')
    return json.load(json_fp)


def dict_write_to_csv(data_list, path):
    with open(path, 'w', encoding='utf-8', newline='') as cf:
        writer = csv.writer(cf)
        for index, i in enumerate(data_list):
            for k in i.keys():
                if i[k] is None or i[k] is 'null':
                    i[k]: ''
            if index == 0:
                writer.writerow(i.keys())
            writer.writerow(i.values())


def timestamp_convert(timestamp, sdf):
    if timestamp == '':
        return ''
    i = int(timestamp)/1000
    t = time.localtime(i)
    return time.strftime(sdf, t)


if __name__ == '__main__':
    cata_zjg_list = csv_analysis_to_dict_list("E:\\io915\\cata_zjg.csv")
    inforesource_report_status_dict = csv_analysis_to_dict("E:\\io915\\inforesource_report.csv", 'ref_info_id', 'status')
    res_list = []
    for c in cata_zjg_list:
        if c['info_resource_life_cycle'] == '7':
            continue
        c['report_status'] = status_dict.get(inforesource_report_status_dict.get(c['cata_id'], ''), '省级未上报')
        c['create_date'] = timestamp_convert(c['create_date'], '%Y-%m-%d %H:%M:%S')
        c['info_resource_life_cycle'] = life_cycle_dict[c['info_resource_life_cycle']]
        res_list.append(c)
    dict_write_to_csv(res_list, "E:\\io915\\output.csv")