# 接口订阅次数修改脚本
# 填写需要修改的相关信息
import datetime

import pymongo
import redis as redis
from bson import ObjectId

# 接口资源名
resource_names = ['苏州大市彩色底图查询']
# 要修改的匹配方式
target_url_map_mode = 'prefix'

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



if __name__ == '__main__':
    print('change task started at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    for resource_name in resource_names:
        api_resource = api_data_resource_collection.find_one({'api_name': resource_name})
        if api_resource is None:
            print('cannot find api_resource!')
        api_resource_api_gateway = api_resource['apiGatewayEntity']
        if api_resource_api_gateway is None:
            print('cannot find api_resource_api_gateway!')
        # 获取网关api实体信息的apiId(非api资源的主键也非网关api实体的主键， 是apiId(注意大小写，在共享mongo中是蛇形，在网关mongo中是驼峰))
        api_gateway_api_id = api_resource_api_gateway['api_id']

        # 更新网关接口
        result = gw_api_info_collection.update_many(
            {'apiId': api_gateway_api_id},
            {'$set': {'urlMapMode': target_url_map_mode}})
        print('gateway_update_res=' + str(result.modified_count))

        # 更新接口资源
        result = api_data_resource_collection.update_one(
            {'api_name': resource_name},
            {'$set': {'url_map_mode': target_url_map_mode, 'apiGatewayEntity.url_map_mode':target_url_map_mode}})
        print('api_data_res_update_res=' + str(result.modified_count))




    redis_client.set("API_INFO_LATEST_DATE", 0)
    print("refresh redis cache complete!")

    print('change task complete at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))