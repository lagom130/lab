# 接口移除限流
# 填写需要修改的相关信息
import datetime

import pymongo
import redis as redis
from bson import ObjectId


api_names = ['省内通办-获取业务项目录接口',
             '省内通办-获取业务办理项',
             '省内通办-获取办件基本信息',
             '省内通办-推送办件补正结果',
             '省内通办-推送办件补正信息',
             '省内通办-推送办件附件信息',
             '省内通办-推送办件结果信息',
             '省内通办-推送办件过程信息',
             '省内通办-推送办件基本信息',
             '省内通办-办件获取成功回执标示',
             '省内通办-获取办件补正信息',
             '省内通办-获取办件附件信息',
             '省内通办-获取办件结果信息',
             '省内通办-获取办件过程信息',
             '省内通办-业务流水号生成',
             '省内通办-获取办理点信息'
             ]

# 配置环境,dev与生产连接方式略有不同
# dev
# mongo_client = pymongo.MongoClient(host="mongo-0.mongo,mongo-1.mongo,mongo-2.mongo`", port=27017)
# mongo_client.admin.authenticate('admin', '123@abcd', mechanism='SCRAM-SHA-1')
# redis_client = redis.StrictRedis(host='redis-master', port=6379, db=5, password='123@abcd')
# 生产
mongo_client = pymongo.MongoClient("192.168.11.111", 27017, username='admin', password='123@abcd',
                                   directConnection=True)
redis_client = redis.StrictRedis(host='192.168.11.111', port=6379, db=5, password='123@abcd')

# mongo 库
data_share_mongo_db = mongo_client["data_share_db"]
cmp_catalog_mongo_db = mongo_client["cmp_catalog"]
dgp_api_gateway_mgt_dsp_mongo_db = mongo_client["dgp_api_gateway_mgt_dsp"]

# ds mongo 集合
api_data_resource_collection = data_share_mongo_db["api_data_resource"]

# api gateway mongo 集合
gw_api_info_collection = dgp_api_gateway_mgt_dsp_mongo_db["gw_api_info"]
gw_api_permission_collection = dgp_api_gateway_mgt_dsp_mongo_db["gw_api_permission"]




# 删除限流
def api_rate_del(api_name):
    # api资源
    api_resource = api_data_resource_collection.find_one({"api_name": api_name})
    if api_resource is None:
        print('cannot find api_resource!')
        return False
    api_resource_api_gateway = api_resource['apiGatewayEntity']
    if api_resource_api_gateway is None:
        print('cannot find api_resource_api_gateway!')
    # 获取网关api实体信息的apiId(非api资源的主键也非网关api实体的主键， 是apiId(注意大小写，在共享mongo中是蛇形，在网关mongo中是驼峰))
    api_resource_api_gateway['max_rate_sec'] = 0
    api_resource_api_gateway['max_rate_day'] = 0
    api_gateway_api_id = api_resource_api_gateway['api_id']
    gw_api_info_collection.update_one({'apiId': api_gateway_api_id}, {'$set':{"maxApiRateEachDay": "0",
    "maxApiRateEachHour": "0",
    "maxApiRateEachMinute": "0",
    "maxApiRateEachMonth": "0",
    "maxApiRateEachSecond": "0"}})


if __name__ == '__main__':
    print('analysis task started at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    for api_name in api_names:
        api_rate_del(api_name)
    redis_client.set("API_INFO_LATEST_DATE", 0)
    print("refresh redis cache complete!")
    print('analysis task complete at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))