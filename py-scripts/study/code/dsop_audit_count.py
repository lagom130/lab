import csv
import re
import time
import datetime

import pymongo
import pymysql
from bson import ObjectId

# dev
# mysql_conn = pymysql.connect(host="mysql-master", port=3306, user='bigdata', password='123@abcd', charset='utf8mb4')
# mongo_client = pymongo.MongoClient(host="mongo-0.mongo,mongo-1.mongo,mongo-2.mongo`", port=27017)
# mongo_client.admin.authenticate('admin', '123@abcd', mechanism='SCRAM-SHA-1')
# 生产
mysql_conn = pymysql.connect(host="2.46.2.102", port=3306, user='bigdata', password='123@abcd', charset='utf8mb4')
mongo_client = pymongo.MongoClient("192.168.11.111", 27017, username='admin', password='123@abcd',
                                   directConnection=True)
# mysql 字典迭代器
cursor = mysql_conn.cursor(cursor=pymysql.cursors.DictCursor)

# mongo 库
data_share_mongo_db = mongo_client["data_share_db"]
cmp_catalog_mongo_db = mongo_client["cmp_catalog"]

# ds mongo 集合
data_resource_apply_collection = data_share_mongo_db["data_resource_apply"]
api_data_resource_collection = data_share_mongo_db["api_data_resource"]
file_data_resource_collection = data_share_mongo_db["file_data_resource"]
table_data_resource_collection = data_share_mongo_db["table_data_resource"]
operation_record_collection = data_share_mongo_db["operation_record"]
# cmp mongo 集合
info_resource_log_collection = cmp_catalog_mongo_db["infoResOPLogEntity"]

# 已发布的市级信息资源 (code为3070150500开头, 生命周期3,4,5)
shiji_yifabu_mulu_sql = "select id, info_resource_name, info_resource_provider,create_date from cmp_catalog.info_resource_platform where (dept_info_resource_code like '3070150500%' or theme_info_resource_code like '3070150500%' or base_info_resource_code like '3070150500%') and info_resource_life_cycle in ('3','4','5')"
# 已发布的区县信息资源 (code为30701505开头且不为3070150500开头, 生命周期3,4,5)
quxian_yifabu_mulu_sql = "select id, info_resource_name, info_resource_provider,create_date from cmp_catalog.info_resource_platform where (dept_info_resource_code like '30701505%' or theme_info_resource_code like '30701505%' or base_info_resource_code like '30701505%') and !(dept_info_resource_code like '3070150500%' or theme_info_resource_code like '3070150500%' or base_info_resource_code like '3070150500%') and info_resource_life_cycle in ('3','4','5')"

# 已发布的市级共享资源(信息资源code为3070150500开头, 生命周期published)
shiji_yifabu_ziyuan_sql = "SELECT id, resource_id, resource_type, resource_name, info_resource_name, status, creater_dep_name, created_time FROM `data_share_db`.`share_data_resource` where status ='published' and info_resource_id in (select id from cmp_catalog.info_resource_platform where (dept_info_resource_code like '3070150500%' or theme_info_resource_code like '3070150500%' or base_info_resource_code like '3070150500%'))"
# 已发布的区县共享资源(信息资源code为30701505开头且不为3070150500开头, 生命周期published)
quxian_yifabu_ziyuan_sql = "SELECT id, resource_id, resource_type, resource_name, info_resource_name, status, creater_dep_name, created_time FROM `data_share_db`.`share_data_resource` where status ='published' and info_resource_id in (select id from cmp_catalog.info_resource_platform where (dept_info_resource_code like '30701505%' or theme_info_resource_code like '30701505%' or base_info_resource_code like '30701505%') and !(dept_info_resource_code like '3070150500%' or theme_info_resource_code like '3070150500%' or base_info_resource_code like '3070150500%'))"


# cmp 操作记录字典k: infoResourceId v:logs
def get_cmp_log():
    # k: infoResourceId v:logs
    logs_dict = {}
    operation_records = info_resource_log_collection.find({})

    for log in operation_records:
        key = log.get('infoResourceId', '')
        if key == '':
            continue
        logs = logs_dict.get(key, [])
        logs.append(log)
        logs_dict[key] = logs

    return logs_dict


# data share 操作记录字典，包含资源与申请 k: data_type-data_id v:logs
def get_operation_records():
    # k: data_type-data_id v:logs
    logs_dict = {}
    operation_records = operation_record_collection.find({})

    for log in operation_records:
        key = log['data_type'] + '-' + log['data_id']
        logs = logs_dict.get(key, [])
        logs.append(log)
        logs_dict[key] = logs

    return logs_dict


# 获取共享资源字典，补全查询维度
def get_resource_dict():
    data_resource_dict = {}
    api_data_resources = api_data_resource_collection.find({})
    for api_data_resource in api_data_resources:
        key = 'API-' + str(api_data_resource['_id'])
        data_resource_dict[key] = {
            'resource_name': api_data_resource.get('api_name', ''),
            'info_resource_name': api_data_resource.get('info_resource_name', '')
        }
    file_data_resources = file_data_resource_collection.find({})
    for file_data_resource in file_data_resources:
        key = 'FILE-' + str(file_data_resource['_id'])
        data_resource_dict[key] = {
            'resource_name': file_data_resource.get('file_name', ''),
            'info_resource_name': file_data_resource.get('info_resource_name', '')
        }
    table_data_resources = table_data_resource_collection.find({})
    for table_data_resource in table_data_resources:
        key = 'TABLE-' + str(table_data_resource['_id'])
        data_resource_dict[key] = {
            'resource_name': table_data_resource.get('table_name', ''),
            'info_resource_name': table_data_resource.get('info_resource_name', '')
        }
    return data_resource_dict


# 获取申请审核记录, 根据operation_record中记录获取
def get_apply_audit_list(logs_dict, data_resource_dict):
    applies = data_resource_apply_collection.find({})
    res_list = []
    for apply in applies:
        resource_type = apply.get('apply_type', '')
        resource_id = apply.get('resource_id', '')
        if resource_id == '':
            print("unknown resource apply" + str(apply))
            continue
        data_resource = data_resource_dict.get(resource_type + "-" + resource_id,
                                               {"resource_name": "", "info_resource_name": ""})
        info_resource_name = data_resource.get('info_resource_name', )
        apply_res = {
            "申请方": apply.get('applicant_unit', ''),
            "共享资源名称": apply.get('resource_name', ''),
            "所属目录": info_resource_name,
            "提供方": apply.get('data_creater_dep_name', ''),
            "申请状态": get_apply_status(apply.get('status', '')),
            "发起申请时间": "",
            "平台管理员审核时间": "",
            "提供方审核时间": "",
        }
        apply_id = str(apply['_id'])
        for log in logs_dict.get('shareResourceApply-' + apply_id, []):
            if log['data_status'] == 'FILE|unAudit' or log['data_status'] == 'TABLE|unAudit' or log[
                'data_status'] == 'API|unAudit':
                apply_res['发起申请时间'] = log['created_time']
            if log['data_status'] == 'platformAudit|true' or log['data_status'] == 'platformAudit|false':
                apply_res['平台管理员审核时间'] = log['created_time']
            if log['data_status'] == 'FILE|unSubscrib' or log['data_status'] == 'TABLE|unSubscrib' or log[
                'data_status'] == 'API|unSubscrib':
                apply_res['提供方审核时间'] = log['created_time']
        res_list.append(apply_res)
    return res_list


# 获取共享资源审核记录, 根据operation_record中记录获取
def get_data_share_audit_list(sql, logs_dict, data_resource_dict):
    data_share_list = get_mysql_res(sql)
    res_list = []
    for data_share in data_share_list:

        resource_type = data_share['resource_type']
        share_resource_id = data_share['id']
        resource_id = data_share.get('resource_id', '')
        if resource_id == '':
            # 打印异常脏数据
            print("unknown resource" + data_share)
        resource_name = data_share.get('resource_name', '')
        info_resource_name = data_share.get('info_resource_name', '')
        operation_records = []
        data_resource = data_resource_dict.get(resource_type + "-" + resource_id,
                                               {"resource_name": "", "info_resource_name": ""})
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
            "所属目录": data_share.get('info_resource_name', info_resource_name),
            "共享资源发布状态": '已发布',
            "提供方": data_share["creater_dep_name"],
            "申请发布时间": '',
            "平台管理员审核时间": '',
        }
        for log in operation_records:
            if log['data_status'] == 'created' or log['data_status'] == 'publishAudit':
                resource_res['申请发布时间'] = log['created_time']
            if log['data_status'] == 'published':
                resource_res['平台管理员审核时间'] = log['created_time']
        # 缺省申请发布时间 使用创建时间
        if resource_res['申请发布时间'] == '':
            resource_res['申请发布时间'] = data_share['created_time']
        res_list.append(resource_res)
    return res_list


# 获取信息资源(目录)审核记录, 根据info_resource_log中记录获取
def get_info_resource_audit_list(sql, logs_dict):
    info_resource_dict_list = get_mysql_res(sql)
    info_resource_res_list = []
    for info_resource in info_resource_dict_list:
        info_resource_id = info_resource['id']
        info_resource_res = {
            '目录名称': info_resource['info_resource_name'],
            '目录发布状态': '已发布',
            '提供方': info_resource['info_resource_provider'],
            '申请发布时间': '',
            '平台管理员审核时间': '',
        }
        info_resource_logs = logs_dict.get(info_resource_id, [])
        for log in info_resource_logs:
            if log['operation'] == '申请发布' or log['operation'] == '创建':
                info_resource_res['申请发布时间'] = log['createTime']
            if log['operation'] == '发布':
                info_resource_res['平台管理员审核时间'] = log['createTime']
        # 缺省申请发布时间 使用创建时间
        if info_resource_res['申请发布时间'] == '':
            info_resource_res['申请发布时间'] = timestamp_to_date(info_resource['create_date'] / 1000, '%Y-%m-%d %H:%M:%S')
        info_resource_res_list.append(info_resource_res)
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


# 写入csv
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


# 10位时间戳转格式化日期
def timestamp_to_date(date, format_string="%Y-%m-%d %H:%M:%S"):
    time_array = time.strptime(date, format_string)
    time_stamp = int(time.mktime(time_array))
    return time_stamp


if __name__ == '__main__':
    print('statistical task started at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # cmp 日志提前处理，目录相关统计需要
    print('cmp logs analysis to dict started')
    cmp_logs_dict = get_cmp_log()
    print('cmp logs analysis to dict completed:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # 统计 目录发布审核(市级)
    print('analysis info resource (suzhoushi) started')
    write_csv(get_info_resource_audit_list(shiji_yifabu_mulu_sql, cmp_logs_dict), '目录发布审核(市级).csv')
    print('analysis info resource (suzhoushi) completed:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # 统计 目录发布审核(区县)
    print('analysis info resource (quxian) started')
    write_csv(get_info_resource_audit_list(quxian_yifabu_mulu_sql, cmp_logs_dict), '目录发布审核(区县).csv')
    print('analysis info resource (quxian) completed:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # datashare 日志提前处理，共享资源发布审核和申请统计需要
    print('operation records analysis to dict started')
    ds_logs_dict = get_operation_records()
    print('operation records analysis to dict completed:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # datashare 资源详情提前处理，共享资源发布审核和申请统计需要
    print('data resources analysis to dict started')
    data_resource_dict = get_resource_dict()
    print('data resources analysis to dict completed:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # 统计 共享资源发布审核(市级)
    print('analysis share data resource (suzhoushi) started')
    write_csv(get_data_share_audit_list(shiji_yifabu_ziyuan_sql, ds_logs_dict, data_resource_dict), '共享资源发布审核(市级).csv')
    print('analysis share data resource (suzhoushi) completed:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # 统计 共享资源发布审核(区县)
    print('analysis share data resource (quxian) started')
    write_csv(get_data_share_audit_list(quxian_yifabu_ziyuan_sql, ds_logs_dict, data_resource_dict), '共享资源发布审核(区县).csv')
    print('analysis share data resource (quxian) completed:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # 统计 共享资源申请审核(所有状态的)
    print('analysis resource apply started')
    write_csv(get_apply_audit_list(ds_logs_dict, data_resource_dict), '共享资源申请审核(所有状态的).csv')
    print('analysis resource apply completed:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    print('statistical task completed at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
