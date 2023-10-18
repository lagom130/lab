import csv
import json


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


def str_to_hump(text):
    arr = filter(None, text.lower().split('_'))
    res = ''
    for index, i in enumerate(arr):
        f = i[0].lower()
        if index is not 0:
            f = f.upper()
        res = res + f+i[1:]
    return res

def data_handle(applies, ds_dict, username_dict):
    res = []
    for apply in applies:
        status = apply.get('status', '')
        status_str = ''
        if status in ['','created', 'unAudit','auditReject','handOver']:
            continue
        elif status in ['unSubscrib','unSend','finished']:
            status_str = '正常'
        else:
            status_str = '终止'
        item = {}

        item['用户账号'] = username_dict.get(apply['createrId'], apply['createrId'])
        item['申请单位'] = apply.get('depName', apply.get('dep_name', apply.get('applicantUnit', '')))
        item['申请人姓名'] = apply.get('applyUserName', apply.get('apply_user_name', apply.get('applicantName','')))
        item['申请人电话'] = apply.get('applyUserPhone', apply.get('apply_User_Phone',apply.get('applyUserPhone',"")))
        item['使用单位'] = apply.get('applicantUnit', '')
        item['使用人姓名'] = apply.get('applicantName', '')
        item['使用人电话'] = apply.get('applicantPhone', '')
        item['使用人邮箱'] = apply.get('applicantEmail', '')
        ds = ds_dict.get(apply.get('shareResourceId', ''), {})
        item['资源类型'] = get_data_share_type(ds.get('resourceType', ''))
        item['资源名称'] = ds.get('resourceName', '')
        item['资源目录'] = ds.get('infoResourceName', '')
        item['资源提供方'] = ds.get('infoResourceProvider', '')
        item['使用字段范围'] = apply.get('useRange', '')
        item['使用事由'] = apply.get('originIncident', '')
        item['使用开始时间'] = apply.get('useDateStart', '')
        item['使用结束时间'] = apply.get('useDateEnd', '')
        item['更新周期'] = apply.get('applyUpdateCycle', '')
        use_time = apply.get('useTimeStart', '')+'~'+apply.get('useTimeEnd', '')
        if use_time == "~":
            use_time = ""
        item['使用时段'] = use_time
        item['调用频次'] = apply.get('callFequency', '')
        item['业务系统名称'] = apply.get('businessSysInfo.sysName', '')
        item['业务系统地址'] = apply.get('businessSysInfo.sysIp', '')
        item['系统部署地址'] = apply.get('businessSysInfo.sysLocation', '')
        item['资源使用状态'] = status_str
        # print(item)
        res.append(item)
    return res

def get_data_share_type(str):
    if str == 'API':
        return '接口'
    if str == 'TABLE':
        return '库表'
    if str == 'FILE':
        return '文件'
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

if __name__ == '__main__':
    apply_list = csv_analysis("E:\\io1022\\apply_1022.csv")
    data_share_list = csv_analysis("E:\\io1022\\di1022.csv")
    userinfo_list = csv_analysis("E:\\io1022\\userinfo.csv")
    username_dict = list_to_dict(userinfo_list, 'umId', 'umUserName')
    ds_dict = list_to_dict_full(data_share_list, 'id')
    print("read csv complete")
    data_list = data_handle(apply_list,ds_dict,username_dict )
    # print("start write to json")
    # with open("E:\\io1022\\oiw.json", 'w', encoding='utf-8') as jf:
    #     jf.write(json.dumps(data_list, ensure_ascii=False, indent=2))
    # print("write to json complete")
    with open("E:\\io1022\\apply_qx.csv", 'w', encoding='utf-8', newline='') as cf:
        writer = csv.writer(cf)
        for index, i in enumerate(data_list):
            for k in i.keys():
                if i[k] is None or i[k] is 'null':
                    i[k]: ''
            if index == 0:
                writer.writerow(i.keys())
            writer.writerow(i.values())
    print("end")