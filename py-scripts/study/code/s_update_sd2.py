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

def update_share_range ():
    return "update share_data_resource set share_range "

if __name__ == '__main__':
    sbwy_list = csv_analysis("E:\\io721\\sbwy.csv")
    apply_simple_list = csv_analysis("E:\\io721\\apply_s.csv")
    info_resource_2_sys_list = csv_analysis("E:\\io721\\iid2sys.csv")
    sd_2_ir_id_list = csv_analysis("E:\\io721\\sd2iid.csv")


    iid_sys_map = {}
    for item in info_resource_2_sys_list:
        iid_sys_map[item['id']] = item.get('info_resource_located_sys', '')

    rid_sys_map = {}
    for item in sd_2_ir_id_list:
        rid_sys_map[item['resource_id']] = iid_sys_map.get(item['info_resource_id'], '无')

    sql_list = []
    for item in sbwy_list:
        if item['info_resource_name'] is not '其他危险化学品生产、储存建设项目安全条件审查' and item['']
        data_list.append(data)
    write_csv(data_list, 'E:\\io721\\sheet3.csv')
    print('over')

