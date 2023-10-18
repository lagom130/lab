import csv
import re
import time
import datetime

import pymongo
import pymysql
from bson import ObjectId

mysql_conn = pymysql.connect(host="mysql-master", port=3306, user='bigdata', password='123@abcd', charset='utf8mb4')
cursor = mysql_conn.cursor(cursor=pymysql.cursors.DictCursor)

mongo_client = pymongo.MongoClient(host="mongo-0.mongo,mongo-1.mongo,mongo-2.mongo`", port=27017)
mongo_client.admin.authenticate('admin', '123@abcd', mechanism='SCRAM-SHA-1')

# mongo_client = pymongo.MongoClient("mongo-0.mongo", 27017,username='admin', password='123@abcd', directConnection=True)
data_share_mongo_db = mongo_client["data_share_db"]
cmp_catalog_mongo_db = mongo_client["cmp_catalog"]

data_resource_apply_collection = data_share_mongo_db["data_resource_apply"]
api_data_resource_collection = data_share_mongo_db["api_data_resource"]
file_data_resource_collection = data_share_mongo_db["file_data_resource"]
table_data_resource_collection = data_share_mongo_db["table_data_resource"]
operation_record_collection = data_share_mongo_db["operation_record"]

info_resource_log_collection = cmp_catalog_mongo_db["infoResOPLogEntity"]

shiji_yifabu_mulu_sql = "select id, info_resource_name, info_resource_provider from cmp_catalog.info_resource_platform where (dept_info_resource_code like '3070150500%' or theme_info_resource_code like '3070150500%' or base_info_resource_code like '3070150500%') and info_resource_life_cycle in ('3','4','5')"
quxian_yifabu_mulu_sql = "select id, info_resource_name, info_resource_provider from cmp_catalog.info_resource_platform where (dept_info_resource_code like '30701505%' or theme_info_resource_code like '30701505%' or base_info_resource_code like '30701505%') and !(dept_info_resource_code like '3070150500%' or theme_info_resource_code like '3070150500%' or base_info_resource_code like '3070150500%') and info_resource_life_cycle in ('3','4','5')"

shiji_yifabu_ziyuan_sql = "SELECT id, resource_id, resource_type, resource_name, info_resource_name, status, creater_dep_name FROM `data_share_db`.`share_data_resource` where status ='published' and info_resource_id in (select id from cmp_catalog.info_resource_platform where (dept_info_resource_code like '3070150500%' or theme_info_resource_code like '3070150500%' or base_info_resource_code like '3070150500%'))"
quxian_yifabu_ziyuan_sql = "SELECT id, resource_id, resource_type, resource_name, info_resource_name, status, creater_dep_name FROM `data_share_db`.`share_data_resource` where status ='published' and info_resource_id in (select id from cmp_catalog.info_resource_platform where (dept_info_resource_code like '30701505%' or theme_info_resource_code like '30701505%' or base_info_resource_code like '30701505%') and !(dept_info_resource_code like '3070150500%' or theme_info_resource_code like '3070150500%' or base_info_resource_code like '3070150500%'))"


def get_apply_audit_list():
    applies = data_resource_apply_collection.find({})
    res_list=[]
    for apply in applies:
        resource_type = apply['apply_type']
        resource_id = apply['resource_id']
        info_resource_name = ''
        if resource_type == 'API':
            api_resource = api_data_resource_collection.find_one(
                {'$or': [{'_id': ObjectId(resource_id)}, {'_id': resource_id}]})
            info_resource_name = api_resource.get('info_resource_name', '')
        elif resource_type == 'FILE':
            file_resource = file_data_resource_collection.find_one({'$or':[{'_id':ObjectId(resource_id)},{'_id':resource_id}]})
            info_resource_name = file_resource.get('info_resource_name', '')
        elif resource_type == 'TABLE':
            table_resource = table_data_resource_collection.find_one({'$or':[{'_id':ObjectId(resource_id)},{'_id':resource_id}]})
            info_resource_name = table_resource.get('info_resource_name', '')
        apply_res = {
            "申请方": apply['applicant_unit'],
            "共享资源名称": apply['resource_name'],
            "所属目录": info_resource_name,
            "提供方": apply['data_creater_dep_name'],
            "申请状态": apply['status'],
            "发起申请时间": "",
            "平台管理员审核时间": "",
            "提供方审核时间": "",
        }
        apply_id = apply['_id'].str()
        operation_records = operation_record_collection.find(
            {'data_id': apply_id, 'data_type': 'shareResourceApply'}).sort(
            [('created_time', 1)])
        for log in operation_records:
            if log['data_status'] == 'FILE|unAudit' or log['data_status'] == 'TABLE|unAudit' or log['data_status'] == 'API|unAudit':
                apply_res['发起申请时间'] = log['created_time']
                if log['data_status'] == 'platformAudit|true' or log['data_status'] == 'platformAudit|false':
                    apply_res['平台管理员审核时间'] = log['created_time']
            if log['data_status'] == 'FILE|unSubscrib' or log['data_status'] == 'TABLE|unSubscrib' or log['data_status'] == 'API|unSubscrib':
                apply_res['提供方审核时间'] = log['created_time']
        res_list.append(apply_res)


def get_data_share_audit_list(sql):
    data_share_list = get_mysql_res(sql)
    res_list = []
    for data_share in data_share_list:

        resource_type = data_share['resource_type']
        share_resource_id = data_share['id']
        resource_id = data_share['resource_id']
        resource_name = data_share.get('resource_name', '')
        info_resource_name = data_share.get('info_resource_name', '')
        operation_records = []
        if resource_type == 'API':
            # api_resource = api_data_resource_collection.find_one({'$or':[{'_id':ObjectId(resource_id)},{'_id':resource_id}]})
            # resource_name = api_resource.get('api_name', resource_name)
            # info_resource_name = api_resource.get('info_resource_name', '')
            operation_records = operation_record_collection.find(
                {'data_id': {'$in': [share_resource_id, resource_id]}, 'data_type': 'shareDataApi'}).sort(
                [('created_time', 1)])
        elif resource_type == 'FILE':
            # file_resource = file_data_resource_collection.find_one({'$or':[{'_id':ObjectId(resource_id)},{'_id':resource_id}]})
            # resource_name = file_resource.get('file_name', resource_name)
            # info_resource_name = file_resource.get('info_resource_name', '')
            operation_records = operation_record_collection.find(
                {'data_id': {'$in': [share_resource_id, resource_id]}, 'data_type': 'shareDataTable'}).sort(
                [('created_time', 1)])
        elif resource_type == 'TABLE':
            # table_resource = table_data_resource_collection.find_one({'$or':[{'_id':ObjectId(resource_id)},{'_id':resource_id}]})
            # resource_name = table_resource.get('table_name', resource_name)
            # info_resource_name = table_resource.get('info_resource_name', '')
            operation_records = operation_record_collection.find(
                {'data_id': {'$in': [share_resource_id, resource_id]}, 'data_type': 'shareDataFile'}).sort(
                [('created_time', 1)])
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
        res_list.append(resource_res)


def get_info_resource_audit_list(sql):
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
        info_resource_logs = info_resource_log_collection.find({'infoResourceId': info_resource_id}).sort(
            [('createTime', 1)])
        for log in info_resource_logs:
            if log['operation'] == '申请发布' or log['operation'] == '创建':
                info_resource_res['申请发布时间'] = log['createTime']
            if log['operation'] == '发布':
                info_resource_res['平台管理员审核时间'] = log['createTime']
        info_resource_res_list.append(info_resource_res)
    return info_resource_res_list


def get_mysql_res(sql):
    cursor.execute(sql)
    res = cursor.fetchall()
    return res

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
    print('analysis info resource (suzhoushi) started')
    write_csv(get_info_resource_audit_list(shiji_yifabu_mulu_sql), '目录发布审核(市级).csv')
    print('analysis info resource (suzhoushi) completed')
    print('analysis info resource (quxian) started')
    write_csv(get_info_resource_audit_list(quxian_yifabu_mulu_sql), '目录发布审核(区县).csv')
    print('analysis info resource (quxian) completed')
    print('analysis share data resource (suzhoushi) started')
    write_csv(get_data_share_audit_list(shiji_yifabu_ziyuan_sql), '共享资源发布审核(市级).csv')
    print('analysis share data resource (suzhoushi) completed')
    print('analysis share data resource (quxian) started')
    write_csv(get_data_share_audit_list(quxian_yifabu_ziyuan_sql), '共享资源发布审核(区县).csv')
    print('analysis share data resource (quxian) completed')
    print('analysis resource apply started')
    write_csv(get_apply_audit_list(), '共享资源申请审核(所有状态的).csv')
    print('analysis resource apply completed')

