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

def data_handle(user_list, r_dict, org_region_dict):
    res = []
    for user in user_list:
        if user['deptId'] == '':
            continue
        role = '操作员'
        if '管理员' in user['roles']:
            role = '管理员'
        status = '已启用'
        if user['userStatus'] == '1':
            status = '已停用'
        auth_perms = []
        gnqx = []
        rp = r_dict.get(user['umId'])
        if rp is not None:
            auth_perms = rp.get('auth_perms', [])
            if len(auth_perms) > 0:
                for ap in auth_perms:
                    gnqx.append(ap['name'])
        item = {}
        item['区域'] = org_region_dict.get(user['deptName'], '')
        item['部门名称'] = user['deptName']
        item['所属部门科室'] = user['userAttrValue']
        item['用户账号'] = user['umUserName']
        item['账号状态'] = status
        item['账号开启时间'] = user['createTime']
        item['用户名称'] = user['realName']
        item['角色（管理员、操作员）'] = role
        item['手机号'] = user['userMobileNo']
        item['电子邮箱'] = user['userEmailId']
        item['功能权限'] = ','.join(gnqx)
        print(item)
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
    userinfo_list = csv_analysis("E:\\io1022\\userinfo1022.csv")
    org_region_map_list = csv_analysis("E:\\io1022\\org_region_map.csv")
    role_permissions = json_read("E:\\io1022\\role_permission.json")
    role_permission_dict = list_to_dict_full(role_permissions, "creater_id")
    org_region_dict = list_to_dict(org_region_map_list, "orgname", 'regionname')
    print("read csv complete")
    data_list = data_handle(userinfo_list, role_permission_dict, org_region_dict)
    # print("start write to json")
    # with open("E:\\io1022\\oiw.json", 'w', encoding='utf-8') as jf:
    #     jf.write(json.dumps(data_list, ensure_ascii=False, indent=2))
    # print("write to json complete")
    with open("E:\\io1022\\user_qx.csv", 'w', encoding='utf-8', newline='') as cf:
        writer = csv.writer(cf)
        for index, i in enumerate(data_list):
            for k in i.keys():
                if i[k] is None or i[k] is 'null':
                    i[k]: ''
            if index == 0:
                writer.writerow(i.keys())
            writer.writerow(i.values())
    print("end")