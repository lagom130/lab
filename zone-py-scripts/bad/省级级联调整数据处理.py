# 省级级联申请调整，历史数据处理
# 补全来自省级联的资源的source_from（数据来源）、province_auth_flag（省级联整体授权标识）、province_auth_expire（省级联整体授权到期时间）属性
# 以及省级联API资源的certification_type（是否电子证照）属性
import datetime

import pymongo
import pymysql
from bson import ObjectId

env = 'DEV'
# env = 'PROD'
mongo_client = None
cursor = None


def init_envs(env):
    if env == 'PROD':
        mysql_conn = pymysql.connect(host="2.46.2.102", port=3306, user='bigdata', password='123@abcd',
                                     charset='utf8mb4')
        mongo_client = pymongo.MongoClient("2.46.2.239", 27017, username='admin', password='123@abcd',
                                           directConnection=True)
    elif env == 'UAT':
        mysql_conn = pymysql.connect(host="2.46.12.38", port=33309, user='bigdata', password='123@abcd',
                                     charset='utf8mb4')
        mongo_client = pymongo.MongoClient("2.46.12.38", 37020, username='admin', password='123@abcd',
                                           directConnection=True)
    else:
        mysql_conn = pymysql.connect(host="mysql-master", port=3306, user='bigdata', password='123@abcd',
                                     charset='utf8mb4')
        mongo_client = pymongo.MongoClient(host="mongo-0.mongo,mongo-1.mongo,mongo-2.mongo`", port=27017)
        mongo_client.admin.authenticate('admin', '123@abcd', mechanism='SCRAM-SHA-1')
    # mysql 字典迭代器
    cursor = mysql_conn.cursor(cursor=pymysql.cursors.DictCursor)
    return mongo_client, cursor


# 列表转字符串（sql拼接用）
def get_arr_str(arr):
    return "'" + "','".join(arr) + "'"


# mysql查询 返回python dict array
def get_mysql_res(cursor, sql):
    cursor.execute(sql)
    res = cursor.fetchall()
    return res


# mongo查询 返回python dict array
def get_mongo_res(mongo_client, database, collection, query):
    results = mongo_client[database][collection].find(query)
    return list(results)


def query_mongo_by_id(mongo_client, database, collection, id):
    query = {'$or': [{'_id': id}]}
    if isinstance(id, str):
        if ObjectId.is_valid(id):
            query['$or'].append({'_id': ObjectId(id)})
    return mongo_client[database][collection].find_one(query)


def update_mongo_by_id(mongo_client, database, collection, id, updates):
    query = {'$or': [{'_id': id}]}
    if isinstance(id, str):
        if ObjectId.is_valid(id):
            query['$or'].append({'_id': ObjectId(id)})
    return mongo_client[database][collection].update_one(query, {'$set': updates})



# 历史数据处理,补全来自省级联的资源的source_from、province_auth_flag、province_auth_expire和certification_type属性
if __name__ == '__main__':
    mongo_client, cursor = init_envs(env)
    print('env=' + env)
    print('data update started at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    resource_relation_list = get_mongo_res(mongo_client, 'data_share_report_db', 'resource_relation', {})
    for resource_relation in resource_relation_list:
        resource_id = resource_relation.get('resourceId', None)
        if resource_id is None:
            continue
        province_resource_id = resource_relation['provinceResourceId']
        resource_type = resource_relation['resourceType']
        apply_reports = get_mongo_res(mongo_client, 'data_share_report_db', 'apply_report',
                                      {'province_info.resource_id': province_resource_id})
        source_from = True
        province_auth_flag = False
        province_auth_expire = None
        updates = {
            'source_from': 'PROVINCE',
            'province_auth_flag': False,
            'province_auth_expire': None
        }
        if any(apply_report['is_auth'] for apply_report in apply_reports):
            updates['province_auth_flag'] = True
            apply_id = next(
                (apply_report['ref_apply_id'] for apply_report in apply_reports if apply_report.get('is_auth')), None)
            if apply_id is not None:
                apply = query_mongo_by_id(mongo_client, 'data_share_db', 'data_resource_apply', apply_id)
                use_date_end = apply['use_date_end']
                if use_date_end is not None and use_date_end != '':
                    updates['province_auth_expire'] = datetime.strptime(use_date_end+" 23:59:59", '%Y-%m-%d %H:%M:%S').timestamp()*1000+999

        collection = ''
        if resource_type == 'FILE':
            collection = 'file_data_resource'
        elif resource_type == 'TABLE':
            collection = 'table_data_resource'
        else:
            collection = 'api_data_resource'
            api_resource = query_mongo_by_id(mongo_client, 'data_share_db', collection, resource_id)
            info_res_results = get_mysql_res(cursor,
                                             "select certification_type from cmp_catalog.info_resource_platform where id ='" +
                                             api_resource['info_resource_id'] + "'")
            certification_type = next((info_res['certification_type'] for info_res in info_res_results), None)
            if certification_type == '1':
                updates['certification_type'] = True
            else:
                updates['certification_type'] = False
        print(str(resource_id) + " updates:"+str(updates))
        update_mongo_by_id(mongo_client, 'data_share_db', collection, resource_id, updates)
    print('data update completed at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
