# 共享申请记录异常
from datetime import date, timedelta, datetime

from bson import ObjectId
import pymongo


# dev
mongo_client = pymongo.MongoClient(host="mongo-0.mongo,mongo-1.mongo,mongo-2.mongo`", port=27017)
mongo_client.admin.authenticate('admin', '123@abcd', mechanism='SCRAM-SHA-1')
# 生产
# mongo_client = pymongo.MongoClient("2.46.2.239", 27017, username='admin', password='123@abcd', directConnection=True)

data_share_db = mongo_client["data_share_db"]
operation_record_collection = data_share_db["operation_record"]
data_resource_apply_collection = data_share_db["data_resource_apply"]


if __name__ == '__main__':
    pipeline2 ={'status': {'$in': ['invalid']},'_id':{'$in': [ObjectId(''),ObjectId(''),ObjectId('')]}}
    result2 = data_resource_apply_collection.find(pipeline2).sort([('resource_name',1)])
    count = 0
    for apply in result2:
        pipeline = {'data_type': 'shareResourceApply','data_id':str(apply['_id'])}
        result = operation_record_collection.find(pipeline).sort([('data_id',1),('created_time',-1)])
        # apply_ids = []
        all_ids = []
        for doc in result:
            if not doc["data_id"] in all_ids:
                all_ids.append(doc["data_id"])
                exchangeInfo = {}
                if 'exchangeInfo' in apply:
                    exchangeInfo = apply['exchangeInfo']
                    if 'exStatus' in exchangeInfo:
                        if exchangeInfo['exStatus'] == 'Pending':
                            exchangeInfo['exStatus']='Done'
                            apply['exchangeInfo']=exchangeInfo
                count = count+1
                print(count)
                if doc['data_status'].find('unSend') != -1:
                    new_doc = doc
                    new_doc.pop('_id')
                    new_doc['data_status'] = doc['data_status'].split('|')[0]+"|finished"
                    if 'data_creater_dep_name' in apply:
                        new_doc['content'] = apply['data_creater_dep_name']+"推送资源"
                        new_doc['operator_name'] = apply['data_creater_dep_name']
                    else:
                        new_doc['content'] = "推送资源" 
                    if 'created_time' in doc:
                        if type(doc['created_time']) is str:
                            day_time= datetime.strptime(doc['created_time'], '%Y-%m-%d %H:%M:%S') + timedelta(days=1)
                            min_time = day_time + timedelta(minutes=10)
                            new_doc['created_time']=datetime.strftime(min_time, '%Y-%m-%d %H:%M:%S')
                        else:
                            created_time = datetime.strftime(doc['created_time'], '%Y-%m-%d %H:%M:%S')
                            day_time= datetime.strptime(created_time, '%Y-%m-%d %H:%M:%S') + timedelta(days=1)
                            min_time = day_time + timedelta(minutes=10)
                            new_doc['created_time']=datetime.strftime(min_time, '%Y-%m-%d %H:%M:%S')
                    else:
                        new_doc['created_time']=datetime.strftime(datetime.now, '%Y-%m-%d %H:%M:%S')
                    operation_record_collection.insert_one(new_doc)
                    print(apply)
                    data_resource_apply_collection.update_one({'_id': apply['_id']}, {'$set': {'exchangeInfo': exchangeInfo,
                                                                                               'updated_time': new_doc['created_time'],
                                                                                                'status': 'finished'}})
                else:
                    print(apply)
                    data_resource_apply_collection.update_one({'_id': apply['_id']}, {'$set': {'exchangeInfo': exchangeInfo,
                                                                                                'status': 'finished'}})