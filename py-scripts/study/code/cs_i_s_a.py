import csv
import datetime
import json
import os
import time


def csv_analysis(path):
    title = []
    data_list = []
    map_dict = {}

    with open(path, encoding='utf-8') as f:
        reader = csv.reader(f)
        for row_index, row in enumerate(reader):
            if row_index is 0:
                title = row

            else:
                data = {}
                for cell_index, cell in enumerate(row):
                    key = str_to_hump(title[cell_index])
                    data[key] = cell
                data_list.append(data)
    return data_list

def json_read(path):
    json_fp = open(path, "r", encoding='utf-8')
    return json.load(json_fp)

def str_to_hump(text):
    arr = filter(None, text.lower().split('_'))
    res = ''
    for index, i in enumerate(arr):
        f = i[0].lower()
        if index is not 0:
            f = f.upper()
        res = res + f+i[1:]
    return res


def get_data_share_type(str):
    if str == 'API':
        return '接口'
    if str == 'TABLE':
        return '库表'
    if str == 'FILE':
        return '文件'
    return str

def get_info_resource_lifecycle(str):
    if str == '1':
        return '已创建'
    if str == '2':
        return '待审核'
    if str == '3':
        return '已发布'
    if str == '4':
        return '撤销待审核'
    if str == '5':
        return '撤销已驳回'
    if str == '6':
        return '已撤销'
    if str == '7':
        return '已删除'
    return str


def get_data_resource_status(str):
    if str == 'created':
        return '已创建'
    if str == 'publishAudit':
        return '发布待审核'
    if str == 'published':
        return '已发布'
    if str == 'publishRejected':
        return '发布已驳回'
    if str == 'revokeAudit':
        return '撤销待审核'
    if str == 'revoked':
        return '已撤销'
    if str == 'revokeRejected':
        return '撤销已驳回'
    if str == 'closed':
        return '已关闭'
    return str

def get_apply_status(str):
    if str == 'created':
        return '已创建'
    if str == 'unAudit':
        return '待审核'
    if str == 'auditReject':
        return '已退回'
    if str == 'unSubscrib':
        return '已同意'
    if str == 'unSend':
        return '已订阅'
    if str == 'finished':
        return '已完成'
    if str == 'invalid':
        return '失效'
    if str == 'handOver':
        return '转交'
    return str

def list_to_dict(list, key_name, value_name):
    res_dict = {}
    for item in list:
        res_dict[item[key_name]] = item.get(value_name, '')
    return res_dict

def list_to_dict_full(list, key_name):
    res_dict = {}
    for item in list:
        res_dict[item[key_name]] = item
    return res_dict

def list_write_to_csv(list, filename, output_path):
    with open(output_path+filename, 'w', encoding='utf-8', newline='') as cf:
        writer = csv.writer(cf)
        for index, i in enumerate(list):
            for k in i.keys():
                if i[k] is None or i[k] is 'null':
                    i[k]: ''
            if index == 0:
                writer.writerow(i.keys())
            writer.writerow(i.values())
    print('wirte data to '+filename+' complete')
if __name__ == '__main__':
    root_path = "E:\\io1031\\"
    output_root_path = root_path+"output\\"
    if not os.path.exists(output_root_path):
        os.mkdir(output_root_path)
    info_resource_list = csv_analysis(root_path+"cs_inforesource.csv")
    data_resource_list = csv_analysis(root_path+"cs_dataresouce.csv")
    apply_list = csv_analysis(root_path+"cs_be_applied.csv")
    print("read csv complete")
    data_resource_dict_1 = list_to_dict_full(data_resource_list, "resourceId")
    data_resource_dict_2 = list_to_dict_full(data_resource_list, "id")

    print("handle dict complete")
    info_resource_output_list = []
    data_resource_output_list = []
    apply_output_list = []
    for info_resource in info_resource_list:
        pd = info_resource.get('publicDate', '')
        if pd != '':
            pd = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(pd)/1000))
        info_resource_output = {
            '目录名称': info_resource.get('infoResourceName', ''),
            '基础类编码': info_resource.get('baseInfoResourceCode', ''),
            '主题类编码': info_resource.get('themeInfoResourceCode', ''),
            '部门类编码': info_resource.get('deptInfoResourceCode', ''),
            '提供方': info_resource.get('infoResourceProvider', ''),
            '资源状态': get_info_resource_lifecycle(info_resource.get('infoResourceLifeCycle', '')),
            '发布时间': pd
        }
        info_resource_output_list.append(info_resource_output)
    for data_share in data_resource_list:
        data_resource_output_list.append({
            '资源名称': data_share.get('resourceName',''),
            '资源所属目录': data_share.get('infoResourceName', ''),
            '提供方': data_share.get('createrDepName', ''),
            '资源类型': get_data_share_type(data_share.get('resourceType', '')),
            '资源状态': get_data_resource_status(data_share.get('status', '')),
            '发布时间': data_share.get('publishTime', '')
        })
    for apply in apply_list:
        dr = data_resource_dict_1.get(apply.get("resourceId"))
        if dr is None:
            dr = data_resource_dict_2.get(apply.get("resourceId"))
        if dr is None:
            dr = {}
        apply_output_list.append({
            "资源名称": apply["resourceName"],
            "资源类型": get_data_share_type(apply["applyType"]),
            "资源所属目录": dr.get("infoResourceName", ""),
            "申请方": apply['dataCreaterDepName'],
            "提供方": apply['createrDepName'],
            "申请时间": apply["createdTime"],
            "申请状态": get_apply_status(apply["status"])
        })
    list_write_to_csv(info_resource_output_list, '常熟所有状态的目录.csv', output_root_path)
    list_write_to_csv(data_resource_output_list, '常熟所有状态的共享资源.csv', output_root_path)
    list_write_to_csv(apply_output_list, '所有别的部门申请常熟的资源.csv', output_root_path)

    print("end")