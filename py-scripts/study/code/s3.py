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

    data_list = []
    for item in sbwy_list:
        apply_num = 0
        sub_num = 0

        for apply in apply_simple_list:
            if apply['resource_id'] == item['resource_id'] or apply['share_resource_id'] == item['resource_id']:
                apply_num = apply_num+1
                sub_num = sub_num + sub_step(apply['status'])
        data = {
            '填表范围（市本级、县区名称）': item['region_name'],
            '行政区划名称（如：盐城市）': item['region_name'],
            '单位名称': item['creater_dep_name'],
            '数据资源目录名称': item['info_resource_name'],
            '来源系统名称': rid_sys_map.get(item['resource_id'], '无'),
            '信息资源格式（见说明）': item['info_resource_format'],
            '数据所属政务事项': item['task_name'],
            '业务类型（见说明）': item['field_type'],
            '应用场景（见说明）': item['gov_use_scene'],
            '数据是否完整（是/否）': '是',
            '共享类型（见说明）': item['share_range'],
            '更新周期（见说明）': item['update_cycle'],
            '未共享主要原因（见说明）': item['share_condition'],
            '订阅总量': sub_num,
            '被申请次数': apply_num,
            '是否向社会开放（是/否）': '否',
            '开放数据访问量': 0
        }
        data_list.append(data)
    write_csv(data_list, 'E:\\io721\\sheet3.csv')
    print('over')

