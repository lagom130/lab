# 省平台接口从服务编排转直接连接
import datetime
import time

import pymongo
import pymysql
import redis
from bson import ObjectId, objectid

api_resources = [
    '省平台_开具证明查询接口提供给地市调用长三角',
    '省平台_异地贷款使用证明状态查询接口yd03',
    '省平台_异地贷款回执管理回执信息接口',
    '省平台_异地贷款结清回执结清信息接口',
    '省平台_异地贷款贷款台账查询',
]
env = 'DEV'
# env = 'PROD'

receivers = None
mongo_client = None
cursor = None
redis_client = None
province_db = None


def api_resource_handle(api_resource_name):
    # 1. 查询市平台接口资源信息
    api_resource = mongo_client['data_share_db']["api_data_resource"].find_one({'api_name': api_resource_name})
    if api_resource is None:
        print('[error]not find api resource, resource name =' + api_resource_name)
        return
    # 市资源ID
    api_id = str(api_resource['_id'])
    print('source url=' + api_resource['api_url'])
    # 网关api_id(不是主键！)
    gw_api_id = api_resource['apiGatewayEntity']['api_id']
    mongo_client["dgp_api_gateway_mgt_dsp"]['gw_api_info'].find_one()
    # 2. 根据市平台接口资源id查询省市资源关联关系
    resource_relation = mongo_client['data_share_report_db']["resource_relation"].find_one({'resourceId': api_id})
    if resource_relation is None:
        print('[error]not find api resource relation, resource name =' + api_resource_name)
        return
    # 省资源id
    province_resource_id = resource_relation['provinceResourceId']
    # 3. 根据关联关系获取到省平台ID， 查询省下行库,获得url
    province_api_resources = get_province_mysql_res(
        "select url from "+province_db+".resource_operationservice where serviceId='" + province_resource_id+"'")
    if len(province_api_resources) < 1:
        print('[error]not find province api resource, resource name =' + api_resource_name)
        return
    # 省接口url
    province_api_resource_url = province_api_resources[0]['url']
    mapper_url = get_province_url_mapper_url(province_api_resource_url)
    print('api resource[' + api_resource_name + '] changed real url: target_url=' + province_api_resource_url)
    print('api resource[' + api_resource_name + '] changed mapper url: target_url=' + mapper_url)
    # 更新data share api 资源
    mongo_client['data_share_db']["api_data_resource"].update_one(
        {
            '_id': api_resource['_id']
        }, {
            '$set': {
                'api_url': province_api_resource_url,
                'apiGatewayEntity.api_mapped_url': mapper_url,
                'apiGatewayEntity.api_real_url': province_api_resource_url
            }
        })
    # 更新网关 api 信息
    mongo_client["dgp_api_gateway_mgt_dsp"]['gw_api_info'].update_one({
        'apiId':gw_api_id
    }, {
        '$set': {
            'apiMappedUri': mapper_url,
            'apiRealUrl': province_api_resource_url
        }
    })


def init_envs(env):
    if env == 'PROD':
        receivers = ['jason.lu@wingconn.com', 'tommie.chen@wingconn.com', 'fisher.dai@wingconn.com']
        mysql_conn = mysql_conn = pymysql.connect(host="2.46.5.192", port=33066, user='JS_SZ_jlxxk_gxpt',
                                                  password='JS_SZ_jlxxk_gxpt@123', charset='utf8mb4')
        mongo_client = pymongo.MongoClient("2.46.2.239", 27017, username='admin', password='123@abcd',
                                           directConnection=True)
        redis_client = redis.StrictRedis(host='192.168.11.111', port=6379, db=5, password='123@abcd')
        province_db = 'jlxxk'
    else:

        receivers = ['jason.lu@wingconn.com']
        mysql_conn = pymysql.connect(host="mysql-master", port=3306, user='bigdata', password='123@abcd',
                                     charset='utf8mb4')
        mongo_client = pymongo.MongoClient(host="mongo-0.mongo,mongo-1.mongo,mongo-2.mongo`", port=27017)
        mongo_client.admin.authenticate('admin', '123@abcd', mechanism='SCRAM-SHA-1')
        redis_client = redis_client = redis.StrictRedis(host='redis-master', port=6379, db=5, password='123@abcd')
        province_db = 'jlxxk'
    # mysql 字典迭代器
    cursor = mysql_conn.cursor(cursor=pymysql.cursors.DictCursor)
    return mongo_client, cursor, receivers, redis_client,province_db


def get_province_mysql_res(sql):
    cursor.execute(sql)
    res = cursor.fetchall()
    return res


# 省接口url转scs 网关 mapped url
def get_province_url_mapper_url(province_url):
    mapper_url = ''
    str_arr = province_url.split('/')
    start_flag = False
    for s in str_arr:
        if s == 'share':
            start_flag = True
        if start_flag:
            mapper_url = mapper_url + '/' + s
    return mapper_url


if __name__ == '__main__':

    mongo_client, cursor, receivers, redis_client, province_db = init_envs(env)
    for api in api_resources:
        print("======== [" + api + "] start ========")
        api_resource_handle(api)
        print("-------- [" + api + "] end --------")

    redis_client.set("API_INFO_LATEST_DATE", 0)
    print("refresh redis cache complete!")