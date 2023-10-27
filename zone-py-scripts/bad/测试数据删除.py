import datetime
import os
import smtplib
import time
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pymongo
import pymysql
from openpyxl.workbook import Workbook

file_context = '信息资源统计信息'
# env = 'DEV'
env = 'PROD'
receivers = None
mongo_client = None
mysql_conn = None
cursor = None

dep_names = ['测试一局', '测试二局', '测试三局']
# dep_names = ['龙门', '部门22']

# 信息资源
info_resource_sql = "select id, info_resource_name, dept_info_resource_code, base_info_resource_code, theme_info_resource_code, info_resource_provider, info_resource_life_cycle, regioncode from cmp_catalog.info_resource_platform"


def init_envs(env):
    if env == 'PROD':
        receivers = ['jason.lu@wingconn.com', 'tommie.chen@wingconn.com']
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
    return mongo_client, mysql_conn, cursor, receivers


# mysql查询 返回python dict array
def get_mysql_res(sql):
    cursor.execute(sql)
    res = cursor.fetchall()
    return res


# mysql执行
def mysql_execute(sql):
    print("mysql execute : " + sql)
    cursor.execute(sql)
    res = cursor.fetchall()
    return


# 列表转字符串（sql拼接用）
def get_arr_str(arr):
    return "'" + "','".join(arr) + "'"


def get_int_arr_str(arr):
    return ",".join(map(str, arr))


# mongo查询 返回python dict array
def get_mongo_res(mongo_client, database, collection, query, projection=None):
    if projection is None:
        results = mongo_client[database][collection].find(query)
    else:
        results = mongo_client[database][collection].find(query, projection)
    return list(results)


# mongo删除
def mongo_delete_many(mongo_client, database, collection, query):
    print("mongo_delete_many [" + database + "][" + collection + "]")
    print(query)
    result = mongo_client[database][collection].delete_many(query)
    print(result.deleted_count)


if __name__ == '__main__':
    print('env=' + env)
    mongo_client, mysql_conn, cursor, receivers = init_envs(env)
    # 部门列表
    dep_arr = get_mysql_res(
        "select dept_id, dept_name from wso2is_db.org_department where dept_name in (%s)" % get_arr_str(dep_names))
    # 部门ID列表
    dep_ids = [item['dept_id'] for item in dep_arr]
    print("deptIds= " + str(dep_ids))
    # 关联用户列表
    user_dept_arr = get_mysql_res(
        "select user_id, org_dept_id from wso2is_db.org_user_dept where org_dept_id in (%s)" % get_arr_str(dep_ids))
    # user id 列表
    user_ids = [item['user_id'] for item in user_dept_arr]
    print("userIds= " + get_int_arr_str(user_ids))

    # 开始删除
    print('meta data init successful!, start delete task at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("start delete info resource")
    # 1. 删除信息资源
    info_res_list = get_mysql_res(
        "select id from cmp_catalog.info_resource_platform where creater_id in (%s)" % get_int_arr_str(user_ids))
    ir_ids = [item['id'] for item in info_res_list]
    mysql_execute("delete from cmp_catalog.info_resource_platform where creater_id in (%s)" % get_int_arr_str(user_ids))
    # 2. 删除记录
    if len(ir_ids) > 0:
        mongo_delete_many(mongo_client, 'cmp_catalog', 'infoResOPLogEntity', {'infoResourceId': {'$in': ir_ids}})
        mongo_delete_many(mongo_client, 'cmp_catalog', 'InfoResOPLogEntity', {'infoResourceId': {'$in': ir_ids}})
    print("start delete share data res")
    # 3. 删除共享资源与申请
    mysql_execute("delete from data_share_db.share_data_resource where creater_dep_id in (%s)" % get_arr_str(dep_ids))
    apis = get_mongo_res(mongo_client, 'data_share_db', 'api_data_resource', {'creater_dep_id': {'$in': dep_ids}},
                         {'_id': True, 'apiGatewayEntity': True})

    api_ids = [str(item['_id']) for item in apis]
    gateway_api_ids = []
    for item in apis:
        api_gateway_entity = item.get('apiGatewayEntity', {})
        gateway_api_id = api_gateway_entity.get('api_id', None)
        if gateway_api_id is not None:
            gateway_api_ids.append(gateway_api_id)
    mongo_delete_many(mongo_client, 'data_share_db', 'api_data_resource', {'creater_dep_id': {'$in': dep_ids}})
    if len(api_ids) > 0:
        mongo_delete_many(mongo_client, 'data_share_db', 'operation_record', {'data_id': {'$in': api_ids}})
    if len(gateway_api_ids) > 0:
        mongo_delete_many(mongo_client, 'dgp_api_gateway_mgt_dsp', 'gw_api_info', {'apiId': {'$in': gateway_api_ids}})
        mongo_delete_many(mongo_client, 'dgp_api_gateway_mgt_dsp', 'gw_api_permission',
                          {'apiId': {'$in': gateway_api_ids}})

    tables = get_mongo_res(mongo_client, 'data_share_db', 'table_data_resource', {'creater_dep_id': {'$in': dep_ids}},
                           {'_id': True})
    table_ids = [str(item['_id']) for item in tables]
    mongo_delete_many(mongo_client, 'data_share_db', 'table_data_resource', {'creater_dep_id': {'$in': dep_ids}})
    if len(table_ids) > 0:
        mongo_delete_many(mongo_client, 'data_share_db', 'operation_record', {'data_id': {'$in': table_ids}})

    files = get_mongo_res(mongo_client, 'data_share_db', 'file_data_resource', {'creater_dep_id': {'$in': dep_ids}},
                          {'_id': True})
    file_ids = [str(item['_id']) for item in files]
    mongo_delete_many(mongo_client, 'data_share_db', 'file_data_resource', {'creater_dep_id': {'$in': dep_ids}})
    if len(file_ids) > 0:
        mongo_delete_many(mongo_client, 'data_share_db', 'operation_record', {'data_id': {'$in': file_ids}})

    applies = get_mongo_res(mongo_client, 'data_share_db', 'data_resource_apply',
                            {'$or': [{'creater_dep_id': {'$in': dep_ids}}, {'data_creater_dep_id': {'$in': dep_ids}}]},
                            {'_id': True})
    apply_ids = [str(item['_id']) for item in applies]
    mongo_delete_many(mongo_client, 'data_share_db', 'data_resource_apply',
                      {'$or': [{'creater_dep_id': {'$in': dep_ids}}, {'data_creater_dep_id': {'$in': dep_ids}}]})
    if len(apply_ids) > 0:
        mongo_delete_many(mongo_client, 'data_share_db', 'operation_record', {'data_id': {'$in': apply_ids}})

    # 删除预约和预约记录
    share_data_reservation_ids = get_mongo_res(mongo_client, 'cmp_catalog', 'share_data_reservation',
                                             {'$or': [{'dept_id': {'$in': dep_ids}}, {'info_resource_provider': {'$in': dep_names}}]},
                                             {'_id':1})
    if len(share_data_reservation_ids) > 0:
        mongo_delete_many(mongo_client, 'cmp_catalog', 'share_data_reservation',
                          {'$or': [{'dept_id': {'$in': dep_ids}}, {'info_resource_provider': {'$in': dep_names}}]})
    share_data_reservation_records = get_mongo_res(mongo_client, 'cmp_catalog', 'share_data_reservation_record',
                                             {'dept_id': {'$in': dep_ids}},
                                             {'_id':1})
    if len(share_data_reservation_records) > 0:
        mongo_delete_many(mongo_client, 'cmp_catalog', 'share_data_reservation_record',
                                             {'dept_id': {'$in': dep_ids}})
    print('delete task completed at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    mysql_conn.commit()
    mysql_conn.close()
