# 导出异常目录分类
import csv
import json
import time

import pymongo
import pymysql

# dev
# mysql_conn = pymysql.connect(host="mysql-master", port=3306, user='bigdata', password='123@abcd', charset='utf8mb4')
import xlrd

mongo_client = pymongo.MongoClient(host="mongo-0.mongo,mongo-1.mongo,mongo-2.mongo`", port=27017)
mongo_client.admin.authenticate('admin', '123@abcd', mechanism='SCRAM-SHA-1')
# 生产
# mysql_conn = pymysql.connect(host="2.46.2.102", port=3306, user='bigdata', password='123@abcd', charset='utf8mb4')
# mongo_client = pymongo.MongoClient("192.168.11.111", 27017, username='admin', password='123@abcd',
#                                    directConnection=True)
# mysql 字典迭代器
# cursor = mysql_conn.cursor(cursor=pymysql.cursors.DictCursor)

# mongo 库
dms_meta_mongo_db = mongo_client["prod_db_data"]
scs_api_gateway_mongo_db = mongo_client["scs_api_gateway"]
auth_center_mongo_db = mongo_client["auth_center"]
datamidd_svc_mongo_db = mongo_client["datamidd_svc"]

csv_data_title = ['dept', 'project', 'create_time', "c4", "c5", "data_res_id"]
csv_data_list = []
data_list = []


dept_to_projects_dict = {}
project_to_dept_dict = {}
dept_id_to_name_dict = {}
project_id_to_name_dict = {}
project_id_to_create_time_dict = {}
data_res_id_to_catalog_id = {}
data_res_id_to_name = {}
catalog_id_to_role_id = {}
is_sub_data_res_ids = []
csv_data_dict = {}

# 13位时间戳转格式化日期
def timestamp_to_date(time_stamp, format_string="%Y-%m-%d %H:%M:%S"):
    str_date = ''
    try:
        time_array = time.localtime(int(time_stamp/1000))
        str_date = time.strftime(format_string, time_array)
    except Exception as e:
        print('except:', e)
    return str_date

def read_csv(path, title):
    csv_list = []
    with open(path, encoding='utf-8') as f:
        reader = csv.reader(f)
        for row_index, row in enumerate(reader):
            data = {}
            for index, i in enumerate(row):
                data[title[index]] = i
            csv_list.append(data)

    return csv_list


def init_depts_and_projects():
    groups = datamidd_svc_mongo_db['group_info'].find({})
    for group in groups:
        create_time = group.get('create_time', '')
        project_id = str(group['_id'])
        project_name = str(group['group_name'])
        dept_id = str(group['depart_id'])
        dept_name = str(group['depart_name'])
        project_id_to_name_dict[project_id] = project_name
        project_id_to_create_time_dict[project_id] = timestamp_to_date(create_time)
        dept_id_to_name_dict[dept_id] = dept_name
        dept_to_projects_dict.get(dept_id, [])
        projects = dept_to_projects_dict.get(dept_id, [])
        if project_id not in projects:
            projects.append(project_id)
        dept_to_projects_dict[dept_id] = projects
        project_to_dept_dict[project_id] = dept_id


#
# def init_data_resources():
#     data_resources = prod_db_mongo_db['data_resource'].find({}, {"catalog_id": 1, 'name_cn':1, "_id":1})
#     for dr in data_resources:
#         data_res_id_to_catalog_id[str(dr['_id'])] = dr.get('catalog_id', '')
#         data_res_id_to_name[str(dr['_id'])] = dr.get('name_cn', '')
#     auths = prod_db_mongo_db['data_manage_authorize'].find({})
#     for auth in auths:
#         catalog_id_to_role_id[str(auth.get('resource_catalog_id', ''))] = str(auth.get('role_id', ''))




# def handle():
#     apis = prod_db_mongo_db['resource_scs_tmp2'].find({}, {"scs_api_name": 1, "data_res_id":1, "app_names":1, "is_subscribed":1, "catalog_id":1, "_id":0})
#     for api in apis:
#         api_name = api.get('scs_api_name','')
#         data_res_id = str(api.get('data_res_id',''))
#         data_res_name = data_res_id_to_name.get(data_res_id, '')
#         app_names = api.get('app_names', '')
#         if app_names is None:
#             app_names = ''
#         app_names = app_names.replace(',', "、")
#         is_sub = api.get('is_subscribed', '')
#         catalog_id = api.get('catalog_id', '')
#         role_id = catalog_id_to_role_id.get(catalog_id, '')
#         dept_name = dept_id_to_name_dict.get(role_id, '')
#         project_id = ''
#         if dept_name == '':
#             project_id = role_id
#             project_name = project_id_to_name_dict.get(role_id, '')
#             dept_id = project_to_dept_dict.get(role_id, '')
#             dept_name = dept_id_to_name_dict.get(dept_id, '')
#         res = {
#             '部门名称': dept_name,
#             '项目名称': project_name,
#             '项目创建时间': project_id_to_create_time_dict.get(project_id),
#             '数据资源名称': data_res_name,
#             '发布的API服务名称': api_name,
#             'API服务是否被订阅': is_sub,
#             '订阅应用的名称': app_names,
#         }
#         csv_item = csv_data_dict.get(data_res_id, {})
#         if res['部门名称'] == '':
#             res['部门名称'] = csv_item.get('dept','')
#         if res['项目名称'] == '':
#             res['项目名称'] = csv_item.get('project', '')
#         if res['项目创建时间'] is None or res['项目创建时间'] == '':
#             res['项目创建时间'] = csv_item.get('create_time', '')
#         # if res['数据资源名称'] == '':
#         #     res['数据资源名称'] = csv_item.get('c5', '')
#         data_list.append(res)
#         is_sub_data_res_ids.append(data_res_id)
#     for did in data_res_id_to_name.keys():
#         if did not in is_sub_data_res_ids:
#             csv_item = csv_data_dict.get(did, {})
#             res = {
#                 '部门名称': csv_item.get('dept', ''),
#                 '项目名称': csv_item.get('project', ''),
#                 '项目创建时间': csv_item.get('create_time', ''),
#                 '数据资源名称': data_res_id_to_name.get(did, ''),
#                 '发布的API服务名称': '',
#                 'API服务是否被订阅': '否',
#                 '订阅应用的名称': '',
#             }
#             data_list.append(res)


# 字典数组写入csv（根据第一条数据获取属性名生成表头）
def write_csv(data_list, path):
    with open(path, 'w', encoding='utf-8', newline='') as cf:
        writer = csv.writer(cf)
        if data_list is not None:
            first_row = data_list[0]
            writer.writerow(first_row.keys())
            for i in data_list:
                for k in i.keys():
                    if i[k] is None or i[k] is 'null':
                        i[k]: ''
                writer.writerow(i.values())


if __name__ == '__main__':
    # csv_data_list = read_csv('E:\\io1205\\1.csv', csv_data_title)
    # for cd in csv_data_list:
    #     splits = cd.get("data_res_id").split('"')
    #     data_res_id = splits[0]
    #     cd["data_res_id"] = data_res_id
    #     csv_data_dict[data_res_id] = cd
    init_depts_and_projects()
    print(dept_to_projects_dict)
    # init_data_resources()
    # handle()
    # write_csv(data_list, 'E:\\io1205\\数据中台接口统计.csv')

