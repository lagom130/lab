# 共享申请记录异常
import datetime
import time

from bson import ObjectId
import pymongo
import csv


# dev
mongo_client = pymongo.MongoClient(host="mongo-0.mongo,mongo-1.mongo,mongo-2.mongo`", port=27017)
mongo_client.admin.authenticate('admin', '123@abcd', mechanism='SCRAM-SHA-1')
# 生产
# mongo_client = pymongo.MongoClient("2.46.2.239", 27017, username='admin', password='123@abcd', directConnection=True)

data_share_db = mongo_client["data_share_db"]
operation_record_collection = data_share_db["operation_record"]
data_resource_apply_collection = data_share_db["data_resource_apply"]

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
    # 根据字段分组条件查询
    pipeline = [
        {'$match': {'data_type': 'shareResourceApply'}},
        {'$group': {'_id': '$data_id', 'count': {'$sum': 1}}},
        {'$match': {'count': {'$gt': 0}}}
    ]
    result = operation_record_collection.aggregate(pipeline)

    apply_ids = []
    # 获取所有申请记录id
    for doc in result:
        subpipeline = {'data_id': doc["_id"]}
        subresult = operation_record_collection.find(subpipeline).sort([('created_time',1)])
        if subresult[0]['data_status'].find('unAudit') == -1:
            apply_ids.append(ObjectId(subresult[0]["data_id"]))

    print(apply_ids)
    # # 根据字段 in范围查询
    # pipeline ={'_id': {'$nin': apply_ids}, 'status': {'$ne': 'created'}}
    pipeline ={'_id': {'$in': apply_ids}}
    result = data_resource_apply_collection.find(pipeline)
    # for doc in result:
    #     print(doc)
    print('export to csv started at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    write_csv(result, "申请审核记录异常.csv")
    print('export to csv completed at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))