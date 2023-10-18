import csv
import json
import os
import csv
import time


status_dict = {"created":"已创建","releaseWaitingApproval": "发布待审核", "revoked": "已撤销", "released": "已发布", "releaseAlreadyReturn": "发布被驳回","expired": "已失效", "DELETE": "已删除"}



def csv_analysis_to_dict(path):
    name_arr = []
    with open(path, encoding='utf-8') as f:
        reader = csv.reader(f)
        for row_index, row in enumerate(reader):
            name_arr.append(row[0])
    return name_arr


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

    in_dict = csv_analysis_to_dict("E:\\io922\\c.csv")
    idc={}
    for name in in_dict:
        idc[name] = idc.get(name, 0)+1
    sql = "select * FROM cmp_catalog.info_resource_platform i WHERE i.info_resource_life_cycle ='0' and  i.info_resource_name in("
    for name in in_dict:
        sql = sql+ "\'"+name+"\',"
    sql= sql[0:(len(sql)-1)]
    sql = sql + ")"
    print(sql)