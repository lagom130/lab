# 接口订阅次数修改脚本
# 填写需要修改的相关信息
import datetime

import pymongo
import redis as redis
from bson import ObjectId

# 申请的资源名
resource_name = '人社输出公积金查询参保'
# 申请方部门(可模糊)
apply_dep_name = '苏州市住房公积金管理中心'
# 提供方部门(可模糊)
provider_dep_name = '苏州市人力资源和社会保障局'
# 要修改成的次数，数据库中都是字符串，要用字符串
target_call_fequency = '864000'

# 配置环境,dev与生产连接方式略有不同
# dev
mongo_client = pymongo.MongoClient(host="mongo-0.mongo,mongo-1.mongo,mongo-2.mongo`", port=27017)
mongo_client.admin.authenticate('admin', '123@abcd', mechanism='SCRAM-SHA-1')
redis_client = redis.StrictRedis(host='redis-master', port=6379, db=5, password='123@abcd')
# 生产
# mongo_client = pymongo.MongoClient("192.168.11.111", 27017, username='admin', password='123@abcd',
#                                    directConnection=True)
# redis_client = redis.StrictRedis(host='192.168.11.111', port=6379, db=5, password='123@abcd')

# mongo 库
data_share_mongo_db = mongo_client["data_share_db"]
cmp_catalog_mongo_db = mongo_client["cmp_catalog"]
dgp_api_gateway_mgt_dsp_mongo_db = mongo_client["dgp_api_gateway_mgt_dsp"]

# ds mongo 集合
data_resource_apply_collection = data_share_mongo_db["data_resource_apply"]
api_data_resource_collection = data_share_mongo_db["api_data_resource"]
table_dept_app_data_collection = data_share_mongo_db["table_dept_app_data"]

# api gateway mongo 集合
gw_api_info_collection = dgp_api_gateway_mgt_dsp_mongo_db["gw_api_info"]
gw_api_permission_collection = dgp_api_gateway_mgt_dsp_mongo_db["gw_api_permission"]


# 根据资源名称、申请方、提供方，修改申请调用次数(str)
def change_apply_call_fequency(resource_name, apply_dep_name, provider_dep_name, target_call_fequency):
    # 查询需要修改的申请
    apply = data_resource_apply_collection.find_one(
        {'resource_name': resource_name, 'dep_name': {'$regex': apply_dep_name},
         'data_creater_dep_name': {'$regex': provider_dep_name}})
    if apply is None:
        print('cannot find apply!')
        return False
    # 申请的api资源的ID
    resource_id = apply['resource_id']
    # 原申请的调用次数, 数据库中是string
    call_fequency = apply['call_fequency']
    # 申请订阅的”部门应用ID“(非”应用的ID(appId)“)
    dept_app_id_list = apply['dept_app_id_list']
    # 申请订阅的”部门应用ID“列表转换为部门应用ObjectId列表
    dept_app_oid_list = []
    for dept_app_id in dept_app_id_list:
        dept_app_oid_list.append(ObjectId(dept_app_id))
    # 查询申请订阅的”部门应用“,获取他们的”应用ID“(即网关使用的appId)
    dept_apps = table_dept_app_data_collection.find({'_id': {'$in': dept_app_oid_list}})
    # 这个才是网关中应用的ID列表
    app_ids = []
    for dept_app in dept_apps:
        app_id = dept_app['app_id']
        app_ids.append(app_id)

    # 查询api资源, 获取网关api实体信息
    api_resource = api_data_resource_collection.find_one({'_id': ObjectId(resource_id)})
    if api_resource is None:
        print('cannot find api_resource!')
        return False
    api_resource_api_gateway = api_resource['apiGatewayEntity']
    if api_resource_api_gateway is None:
        print('cannot find api_resource_api_gateway!')
    # 获取网关api实体信息的apiId(非api资源的主键也非网关api实体的主键， 是apiId(注意大小写，在共享mongo中是蛇形，在网关mongo中是驼峰))
    api_gateway_api_id = api_resource_api_gateway['api_id']
    # 授权列表
    permissions = gw_api_permission_collection.find({'apiId': api_gateway_api_id, 'appId': {'$in': app_ids}})
    for permission in permissions:
        # 数据库中是string
        maxSubAmountEachDay = permission['maxSubAmountEachDay']
        print('apply change call_fequency, api gw permission[apiId:' + permission['apiId'] + '-appId:' + permission[
            'appId'] + 'changes form ' + str(maxSubAmountEachDay) + ' to ' + str(target_call_fequency))
    # 更新网关权限
    permissions_update_res = gw_api_permission_collection.update_many(
        {'apiId': api_gateway_api_id, 'appId': {'$in': app_ids}},
        {'$set': {'maxSubAmountEachDay': target_call_fequency}})
    print('permissions_update_res=' + str(permissions_update_res.modified_count))

    print('apply call_fequency changes from ' + str(call_fequency) + ' to ' + str(target_call_fequency))
    # 更新apply
    apply_update_res = data_resource_apply_collection.update_one(
        {'resource_name': resource_name, 'dep_name': {'$regex': apply_dep_name},
         'data_creater_dep_name': {'$regex': provider_dep_name}}, {'$set': {'call_fequency': target_call_fequency}})
    print('apply_update_res=' + str(apply_update_res.modified_count))
    return True


if __name__ == '__main__':
    print('change task started at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    change_res = change_apply_call_fequency(resource_name, apply_dep_name, provider_dep_name, target_call_fequency)
    if change_res is True:
        # 修改成功，修改redis中权限更新时间戳，使其全量更新缓存
        redis_client.set("API_PERMIT_LATEST_DATE", 0)
        print("refresh redis cache complete!")

    print('change task complete at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))