# 共享审核信息统计脚本
# 导出csv文件到audit.zip，不需要导出的可以在main中注释
# 注意不要注释掉中间处理需要的查询结果
import csv
import os
import time
import datetime
import gc

import pymongo
import pymysql

import zipfile

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.header import Header

# env = 'DEV'
env = 'PROD'
receivers = None
mongo_client = None
cursor = None

# 过滤部门 测试一局、测试二局、测试三局
filter_dep = []
# filter_dep = ['814617580947993160', '814617817852743519', '819426144655375519']

# 市级 region map catalog code
shiji_region_map_catalog_codes = ['0500']

# 区县 region map catalog code
quxian_region_map_catalog_codes = ['0582', '0581', '0585', '0583', '0509', '0506', '0507', '0508', '0590', '0505']

# 信息资源，占位符为region_code
info_resource_sql = "select id, info_resource_name, info_resource_provider,create_date,info_resource_life_cycle, is_open, regioncode, info_item_desc_detail, share_type, related_task_flag, task_type, task_name, basic_catalog_code, business_handling_code, implement_list_code from cmp_catalog.info_resource_platform WHERE regioncode IN (%s)"

# 共享资源mysql查询, 第一个占位符为region_id 第二个占位符为过滤部门列表
data_share_sql = "SELECT id, resource_id, resource_type, resource_name, info_resource_name, status, creater_dep_name, created_time, region_id, share_range FROM `data_share_db`.`share_data_resource`  WHERE region_id IN (%s) AND creater_dep_id NOT IN (%s)"

region_id_to_code_dict = {}

region_code_to_name_dict = {
    "0500": "苏州市",
    "0505": "高新区",
    "0506": "吴中区",
    "0507": "相城区",
    "0508": "姑苏区",
    "0509": "吴江区",
    "0581": "常熟市",
    "0582": "张家港市",
    "0583": "昆山市",
    "0585": "太仓市",
}

resource_type_dict = {
    'API': '接口',
    'TABLE': '库表',
    'FILE': '文件',
    'api': '接口',
    'table': '库表',
    'file': '文件',
}


def init_envs(env):
    if env == 'PROD':
        receivers = ['jason.lu@wingconn.com', 'tommie.chen@wingconn.com','teresa.yang@wingconn.com']
        mysql_conn = pymysql.connect(host="2.46.2.102", port=3306, user='bigdata', password='123@abcd',
                                     charset='utf8mb4')
        mongo_client = pymongo.MongoClient("2.46.2.239", 27017, username='admin', password='123@abcd',
                                           directConnection=True)
    else:

        receivers = ['jason.lu@wingconn.com']
        mysql_conn = pymysql.connect(host="mysql-master", port=3306, user='bigdata', password='123@abcd',
                                     charset='utf8mb4')
        mongo_client = pymongo.MongoClient(host="mongo-0.mongo,mongo-1.mongo,mongo-2.mongo`", port=27017)
        mongo_client.admin.authenticate('admin', '123@abcd', mechanism='SCRAM-SHA-1')
    # mysql 字典迭代器
    cursor = mysql_conn.cursor(cursor=pymysql.cursors.DictCursor)
    return mongo_client, cursor, receivers


# 列表转字符串（sql拼接用）
def get_arr_str(arr):
    return "'" + "','".join(arr) + "'"


def get_region_ids(codes):
    region_catalogs = mongo_client["cmp_catalog"]["map_catalog"].find(
        {'mapCatalogCode': {'$in': codes}, 'mapCatalogType': 'region'},{'_id':True, 'mapCatalogCode':True})
    region_ids = []
    for region in region_catalogs:
        region_ids.append(str(region["_id"]))
        region_id_to_code_dict[str(region["_id"])] = str(region["mapCatalogCode"])
    return region_ids


# cmp 操作记录字典k: infoResourceId v:logs
def get_cmp_log():
    # k: infoResourceId v:logs
    logs_dict = {}
    operation_records = mongo_client["cmp_catalog"]["infoResOPLogEntity"].find({},{'infoResourceId':True, 'operation':True, 'createTime':True})

    for log in operation_records:
        key = log.get('infoResourceId', '')
        if key == '':
            continue
        logs = logs_dict.get(key, [])
        logs.append(log)
        logs_dict[key] = logs
    # 释放内存
    del operation_records
    gc.collect()
    return logs_dict


# data share 操作记录字典，包含资源与申请 k: data_type-data_id v:logs
def get_operation_records(logs_dict, data_type):
    # k: data_type-data_id v:logs
    operation_records = mongo_client["data_share_db"]["operation_record"].find({'data_type':data_type}, {'data_id':True,'data_status':True,'created_time':True,'operator_id':True})
    for log in operation_records:
        key = data_type + '-' + log['data_id']
        logs = logs_dict.get(key, [])
        logs.append(log)
        logs_dict[key] = logs
    del operation_records
    gc.collect()
    return logs_dict


# 获取共享资源字典，补全查询维度
def get_resource_dict():
    info_resource_resource_ids_dict = {}
    data_resource_dict = {}
    api_data_resources = mongo_client["data_share_db"]["api_data_resource"].find(
        {'creater_dep_id': {'$nin': filter_dep}}, {'_id':True, 'api_name':True, 'info_resource_name':True, 'info_items':True})
    for api_data_resource in api_data_resources:
        key = 'API-' + str(api_data_resource['_id'])
        data_resource_dict[key] = {
            'resource_name': api_data_resource.get('api_name', ''),
            'info_resource_name': api_data_resource.get('info_resource_name', ''),
            'resource_item_names': get_item_list_str(api_data_resource, 'info_items', 'item_name'),
            'resource_item_descs': get_item_list_str(api_data_resource, 'info_items', 'item_desc'),
        }
        resource_id = str(api_data_resource['_id'])
        info_resource_id = api_data_resource.get('info_resource_id', '')
        if info_resource_id != '':
            resource_ids = info_resource_resource_ids_dict.get(info_resource_id, [])
            resource_ids.append(resource_id)
            info_resource_resource_ids_dict[info_resource_id] = resource_ids
    # 释放内存
    del api_data_resources
    gc.collect()
    file_data_resources = mongo_client["data_share_db"]["file_data_resource"].find(
        {'creater_dep_id': {'$nin': filter_dep}}, {'_id':True, 'file_name':True, 'info_resource_name':True, 'info_items':True})
    for file_data_resource in file_data_resources:
        key = 'FILE-' + str(file_data_resource['_id'])
        data_resource_dict[key] = {
            'resource_name': file_data_resource.get('file_name', ''),
            'info_resource_name': file_data_resource.get('info_resource_name', ''),
            'resource_item_names': get_item_list_str(file_data_resource, 'info_items', 'item_name'),
            'resource_item_descs': get_item_list_str(file_data_resource, 'info_items', 'item_desc'),
        }
        resource_id = str(file_data_resource['_id'])
        info_resource_id = file_data_resource.get('info_resource_id', '')
        if info_resource_id != '':
            resource_ids = info_resource_resource_ids_dict.get(info_resource_id, [])
            resource_ids.append(resource_id)
            info_resource_resource_ids_dict[info_resource_id] = resource_ids
    # 释放内存
    del file_data_resources
    gc.collect()
    table_data_resources = mongo_client["data_share_db"]["table_data_resource"].find(
        {'creater_dep_id': {'$nin': filter_dep}}, {'_id':True, 'table_name':True, 'info_resource_name':True, 'info_items':True})
    for table_data_resource in table_data_resources:
        key = 'TABLE-' + str(table_data_resource['_id'])
        data_resource_dict[key] = {
            'resource_name': table_data_resource.get('table_name', ''),
            'info_resource_name': table_data_resource.get('info_resource_name', ''),
            'resource_item_names': get_item_list_str(table_data_resource, 'info_items', 'item_name'),
            'resource_item_descs': get_item_list_str(table_data_resource, 'info_items', 'item_desc'),
        }
        resource_id = str(table_data_resource['_id'])
        info_resource_id = table_data_resource.get('info_resource_id', '')
        if info_resource_id != '':
            resource_ids = info_resource_resource_ids_dict.get(info_resource_id, [])
            resource_ids.append(resource_id)
            info_resource_resource_ids_dict[info_resource_id] = resource_ids
    # 释放内存
    del table_data_resources
    gc.collect()
    return data_resource_dict, info_resource_resource_ids_dict


# 获取申请审核记录, 根据operation_record中记录获取
def get_apply_audit_list(data_resource_dict):
    applies = mongo_client["data_share_db"]["data_resource_apply"].find(
        {'data_creater_dep_id': {'$nin': filter_dep}, 'creater_dep_id': {'$nin': filter_dep}})
    res_list = []
    for apply in applies:
        resource_type = apply.get('apply_type', '')
        resource_id = apply.get('resource_id', '')
        if resource_id == '':
            print("unknown resource apply" + str(apply))
            continue
        data_resource = data_resource_dict.get(resource_type + "-" + resource_id,
                                               {"resource_name": "", "info_resource_name": "",
                                                'resource_item_names': '', 'resource_item_descs': ''})
        info_resource_name = data_resource.get('info_resource_name', )
        apply_res = {
            "申请方": apply.get('dep_name', ''),
            "共享资源名称": apply.get('resource_name', ''),
            "共享资源类型": resource_type_dict.get(resource_type, ''),
            "所属目录": info_resource_name,
            "提供方": apply.get('data_creater_dep_name', ''),
            "申请状态": get_apply_status(apply.get('status', '')),
            "发起申请时间": timestamp13_to_date(apply.get('apply_time', None)),
            "平台管理员审核时间": timestamp13_to_date(apply.get('admin_audit_time', None)),
            "提供方审核时间": timestamp13_to_date(apply.get('provider_audit_time', None)),
            "资源信息项名称列表": data_resource.get('resource_item_names', ''),
            "资源信息项说明列表": data_resource.get('resource_item_descs', ''),
            "申请信息项名称列表": get_item_list_str(apply, 'info_items', 'item_name'),
            "申请信息项说明列表": get_item_list_str(apply, 'info_items', 'item_desc'),
        }
        res_list.append(apply_res)
    # 释放内存
    del applies
    gc.collect()
    return res_list


# 获取共享资源审核记录, 根据operation_record中记录获取
def get_data_share_audit_list(sql, logs_dict, data_resource_dict):
    data_share_list = get_mysql_res(sql)
    res_list = []
    for data_share in data_share_list:

        resource_type = data_share['resource_type']
        share_resource_id = data_share['id']
        resource_id = data_share.get('resource_id', '')
        share_range = data_share.get('share_range', '')
        if resource_id == '':
            # 打印异常脏数据
            print("unknown resource" + data_share)
        resource_name = data_share.get('resource_name', '')
        info_resource_name = data_share.get('info_resource_name', '')
        operation_records = []
        data_resource = data_resource_dict.get(resource_type + "-" + resource_id,
                                               {"resource_name": "", "info_resource_name": "",
                                                'resource_item_names': '', 'resource_item_descs': ''})
        info_resource_name = data_resource.get('info_resource_name', info_resource_name)
        resource_name = data_resource.get('resource_name', resource_name)
        if resource_type == 'API':
            operation_records = logs_dict.get('shareDataApi-' + resource_id, [])
            if operation_records is None or len(operation_records) == 0:
                operation_records = logs_dict.get('shareDataApi-' + share_resource_id, [])
        elif resource_type == 'FILE':
            operation_records = logs_dict.get('shareDataFile-' + resource_id, [])
            if operation_records is None or len(operation_records) == 0:
                operation_records = logs_dict.get('shareDataFile-' + share_resource_id, [])
        elif resource_type == 'TABLE':
            operation_records = logs_dict.get('shareDataTable-' + resource_id, [])
            if operation_records is None or len(operation_records) == 0:
                operation_records = logs_dict.get('shareDataTable-' + share_resource_id, [])
        resource_res = {
            "共享资源名称": resource_name,
            "共享资源类型": resource_type_dict.get(resource_type, ''),
            "共享类型": share_range,
            "所属目录": data_share.get('info_resource_name', info_resource_name),
            "共享资源发布状态": get_share_data_resource_status(data_share.get('status', '')),
            "提供方": data_share["creater_dep_name"],
            '提供方属地': region_code_to_name_dict.get(region_id_to_code_dict.get(data_share.get('region_id', ''), ''), ''),
            "申请发布时间": '',
            "平台管理员审核时间": '',
            "资源信息项名称列表": data_resource.get('resource_item_names', ''),
            "资源信息项说明列表": data_resource.get('resource_item_descs', ''),
        }
        sqfbsj = 0
        ptglyshsj = 0
        for log in operation_records:
            if log['data_status'] == 'created' or log['data_status'] == 'publishAudit':
                new_sqfbsj = time.mktime(
                    datetime.datetime.strptime(log['created_time'], '%Y-%m-%d %H:%M:%S').timetuple())
                if new_sqfbsj - sqfbsj > 0:
                    sqfbsj = new_sqfbsj
                    resource_res['申请发布时间'] = log['created_time']
            if log['data_status'] == 'published' or log['data_status'] == 'publishRejected':
                new_ptglyshsj = time.mktime(
                    datetime.datetime.strptime(log['created_time'], '%Y-%m-%d %H:%M:%S').timetuple())
                if new_ptglyshsj - ptglyshsj > 0:
                    ptglyshsj = new_ptglyshsj
                    resource_res['平台管理员审核时间'] = log['created_time']
            if log['data_status'] == 'revoked' and (log['operator_id'] == 'admin' or log['operator_id'] == '0'):
                new_ptglyshsj = time.mktime(
                    datetime.datetime.strptime(log['created_time'], '%Y-%m-%d %H:%M:%S').timetuple())
                if new_ptglyshsj - ptglyshsj > 0:
                    ptglyshsj = new_ptglyshsj
                    resource_res['平台管理员审核时间'] = log['created_time']
        # 缺省申请发布时间 使用创建时间
        if resource_res['申请发布时间'] == '':
            resource_res['申请发布时间'] = data_share['created_time']
        res_list.append(resource_res)
    # 释放内存
    del data_share_list
    gc.collect()
    return res_list


# 获取信息资源(目录)审核记录, 根据info_resource_log中记录获取
def get_info_resource_audit_list(sql, logs_dict, info_resource_resource_ids_dict):
    info_resource_dict_list = get_mysql_res(sql)
    info_resource_res_list = []
    for info_resource in info_resource_dict_list:
        info_resource_id = info_resource['id']
        # info_item_desc_detail = info_resource['info_item_desc_detail']
        share_type = info_resource.get('share_type', '')
        resources = info_resource_resource_ids_dict.get(info_resource_id, [])
        has_resources = '否'
        if len(resources) > 0:
            has_resources = '是'

        related_task_flag = '否'
        related_task_be_complete = '-'
        if info_resource.get('related_task_flag', '') != 0:
            related_task_flag = '是'
            task_type_list = list(filter(None, (info_resource.get('task_type') or "").split("|")))
            task_name_list = list(filter(None, (info_resource.get('task_name') or "").split("|")))
            basic_catalog_code_list = list(filter(None, (info_resource.get('basic_catalog_code') or "").split("|")))
            business_handling_code_list = list(filter(None, (info_resource.get('business_handling_code') or "").split("|")))
            implement_list_code_list = list(filter(None, (info_resource.get('implement_list_code') or "").split("|")))
            if len(task_name_list) == 0:
                related_task_be_complete = '未填'
            else:
                related_task_be_complete = '完整'
                if len(task_type_list) < len(task_name_list) or len(basic_catalog_code_list) < len(task_name_list) or len(business_handling_code_list) < len(task_name_list) or len(implement_list_code_list) < len(task_name_list):
                    related_task_be_complete = '部分'
                else:
                    for index, task_name in enumerate(task_name_list):
                        if not task_name:
                            related_task_be_complete = '部分'
                        if not task_type_list[index]:
                            related_task_be_complete = '部分'
                        if not basic_catalog_code_list[index]:
                            related_task_be_complete = '部分'
                        if not business_handling_code_list[index]:
                            related_task_be_complete = '部分'
                        if not implement_list_code_list[index]:
                            related_task_be_complete = '部分'





        info_resource_res = {
            '目录名称': info_resource['info_resource_name'],
            '目录发布状态': get_info_resource_status(info_resource['info_resource_life_cycle']),
            "共享类型": share_type,
            '提供方': info_resource['info_resource_provider'],
            '提供方属地': region_code_to_name_dict.get(info_resource.get('regioncode', ''), ''),
            '目录下是否挂接资源': has_resources,
            '目录下挂接资源数量': len(resources),
            '是否开放': get_is_open(info_resource.get('is_open', '')),
            '是否关联服务事项': related_task_flag,
            '服务事项是否完整': related_task_be_complete,
            '申请发布时间': '',
            '平台管理员审核时间': '',
        }
        info_resource_logs = logs_dict.get(info_resource_id, [])

        sqfbsj = 0
        ptglyshsj = 0
        for log in info_resource_logs:
            if log['operation'] == '申请发布' or log['operation'] == '创建':
                new_sqfbsj = time.mktime(datetime.datetime.strptime(log['createTime'], '%Y-%m-%d %H:%M:%S').timetuple())
                if new_sqfbsj - sqfbsj > 0:
                    sqfbsj = new_sqfbsj
                    info_resource_res['申请发布时间'] = log['createTime']
            if log['operation'] == '发布' or log['operation'] == '发布退回':
                new_ptglyshsj = time.mktime(
                    datetime.datetime.strptime(log['createTime'], '%Y-%m-%d %H:%M:%S').timetuple())
                if new_ptglyshsj - ptglyshsj > 0:
                    ptglyshsj = new_ptglyshsj
                    info_resource_res['申请发布时间'] = log['createTime']
                info_resource_res['平台管理员审核时间'] = log['createTime']
        # 缺省申请发布时间 使用创建时间
        if info_resource_res['申请发布时间'] == '':
            create_date = info_resource.get('create_date', 0)
            if create_date is not None and create_date > 0:
                info_resource_res['申请发布时间'] = timestamp_to_date(info_resource['create_date'] / 1000,
                                                                '%Y-%m-%d %H:%M:%S')
        info_resource_res_list.append(info_resource_res)
    # 释放内存
    del info_resource_dict_list
    gc.collect()
    return info_resource_res_list


# mysql查询 返回python dict array
def get_mysql_res(sql):
    cursor.execute(sql)
    res = cursor.fetchall()
    return res


# 申请状态转换
def get_apply_status(status):
    if status == 'created':
        return '已创建'
    elif status == 'unAudit':
        return '待审核'
    elif status == 'auditReject':
        return '已退回'
    elif status == 'unSubscrib':
        return '待订阅'
    elif status == 'unSend':
        return '待推送'
    elif status == 'finished':
        return '已完成'
    elif status == 'invalid':
        return '失效'
    elif status == 'handOver':
        return '转交'
    return ''


# 信息资源状态转换
def get_info_resource_status(status):
    if status == '0':
        return '已创建'
    elif status == '1':
        return '发布待审核'
    elif status == '2':
        return '发布已驳回'
    elif status == '3':
        return '已发布'
    elif status == '4':
        return '撤销待审核'
    elif status == '5':
        return '撤销已驳回'
    elif status == '6':
        return '已撤销'
    elif status == '7':
        return '已删除'
    return ''


# 共享资源状态转换
def get_share_data_resource_status(status):
    if status == 'created':
        return '已创建'
    elif status == 'publishAudit':
        return '发布待审核'
    elif status == 'published':
        return '已发布'
    elif status == 'publishRejected':
        return '发布已驳回'
    elif status == 'revokeAudit':
        return '撤销待审核'
    elif status == 'revoked':
        return '已撤销'
    elif status == 'revokeRejected':
        return '撤销已驳回'
    elif status == 'closed':
        return '已关闭'
    return ''


# 是否开放
def get_is_open(str):
    if str == '1':
        return '是'
    else:
        return '否'


# 字典数组写入csv（根据第一条数据获取属性名生成表头）
def write_csv_to_zip(data_list, path, zip_file):
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
    zip_file.write(path)
    os.remove(path)


# 10位时间戳转格式化日期
def timestamp_to_date(time_stamp, format_string="%Y-%m-%d %H:%M:%S"):
    time_array = time.localtime(time_stamp)
    str_date = time.strftime(format_string, time_array)
    return str_date

# 13位时间戳转格式化日期
def timestamp13_to_date(time_stamp, format_string="%Y-%m-%d %H:%M:%S"):
    if time_stamp is None:
        return ''
    time_array = time.localtime(time_stamp/1000)
    str_date = time.strftime(format_string, time_array)
    return str_date

def send_mail():
    smtp_host = 'smtp.163.com'
    port = 25
    sender = 'rikurobot@163.com'
    password = 'BDDHTVARWQRQFPFN'
    # receivers = ['jason.lu@wingconn.com', 'tommie.chen@wingconn.com', 'fisher.dai@wingconn.com']

    sub = Header('[' + env + ']共享平台审核统计' + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), 'utf-8')
    msg = MIMEMultipart()
    msg['Subject'] = sub
    msg['From'] = sender

    part = MIMEText('附件为共享平台审核统计结果，本邮件为自动发送，请勿回复！')
    msg.attach(part)

    part = MIMEApplication(open('audit.zip', 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename='audit.zip')
    msg.attach(part)

    smtp = smtplib.SMTP(smtp_host, port, 'utf-8')
    smtp.login(sender, password)
    smtp.sendmail(sender, receivers, msg.as_string())
    smtp.quit()
    print('send msg successfully!')


def get_item_list_str(dict, key_name, use_key_name):
    items = dict.get(key_name, [])
    res_arr = []
    for item in items:
        res_arr.append(item.get(use_key_name, ''))
    result = list(filter(lambda x: x != '', res_arr))
    return ','.join(result)


# def writeFilesToZip(file_paths, zipFile):
#     for file_path in file_paths:
#         for f in os.listdir():
#
#     for f in os.listdir():
#         os.path
#         absFile=os.path.join(absDir,f) #子文件的绝对路径
#         if os.path.isdir(absFile): #判断是文件夹，继续深度读取。
#             relFile=absFile[len(os.getcwd())+1:] #改成相对路径，否则解压zip是/User/xxx开头的文件。
#             zipFile.write(relFile) #在zip文件中创建文件夹
#             writeAllFileToZip(absFile,zipFile) #递归操作
#         else: #判断是普通文件，直接写到zip文件中。
#             relFile=absFile[len(os.getcwd())+1:] #改成相对路径
#             zipFile.write(relFile)
#     return

# 当前脚本运行时会占用约5G的内存，要警惕oom
# 日志、资源提前全部查询转换为字典放入内存，否则过于频繁的查询数据库（十万级或者百万级的查询次数），效率及其低下，用空间换取时间（数据量上去了有oom的风险）
if __name__ == '__main__':
    mongo_client, cursor, receivers = init_envs(env)
    print('env='+env+', will send to'+str(receivers))
    print('statistical task started at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    zip_file_path = 'audit.zip'
    if os.path.exists(zip_file_path):
        os.remove(zip_file_path)
        print("remove old result")
    zip_file = zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED)

    # datashare 资源详情提前处理，目录、共享资源发布审核和申请统计需要
    print('data resources analysis to dict started')
    data_resource_dict, info_resource_resource_ids_dict = get_resource_dict()
    print('data resources analysis to dict completed:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # cmp 日志提前处理，目录相关统计需要
    print('cmp logs analysis to dict started')
    cmp_logs_dict = get_cmp_log()
    print('cmp logs analysis to dict completed:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # 统计 目录发布审核(市级)
    print('analysis info resource (suzhoushi) started')
    write_csv_to_zip(
        get_info_resource_audit_list(info_resource_sql % get_arr_str(shiji_region_map_catalog_codes), cmp_logs_dict,
                                     info_resource_resource_ids_dict),
        '目录发布审核(市级).csv', zip_file)
    print('analysis info resource (suzhoushi) completed:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # 统计 目录发布审核(区县)
    print('analysis info resource (quxian) started')
    write_csv_to_zip(
        get_info_resource_audit_list(info_resource_sql )