# 共享申请记录异常
from datetime import date, timedelta, datetime

from bson import ObjectId
import pymongo


# dev
mongo_client = pymongo.MongoClient(host="mongo-0.mongo,mongo-1.mongo,mongo-2.mongo`", port=27017)
mongo_client.admin.authenticate('admin', '123@abcd', mechanism='SCRAM-SHA-1')
# 生产
#mongo_client = pymongo.MongoClient("2.46.2.239", 27017, username='admin', password='123@abcd', directConnection=True)

data_share_db = mongo_client["data_share_db"]
operation_record_collection = data_share_db["operation_record"]
data_resource_apply_collection = data_share_db["data_resource_apply"]


if __name__ == '__main__':
    pipeline2 ={'status': {'$in': ['invalid']}}
    result2 = data_resource_apply_collection.find(pipeline2).sort([('resource_name',1)])
    apply_ids=[]
    apply_dic={}
    for doc in result2:
        apply_ids.append(str(doc['_id']))
        apply_dic[str(doc['_id'])] = doc
    count = 0
    pipeline = {'data_type': 'shareResourceApply','data_id':{'$in': apply_ids}}
    result = operation_record_collection.find(pipeline).sort([('data_id',1),('created_time',-1)])
    all_ids = []
    for doc in result:
        if not doc["data_id"] in all_ids:
            all_ids.append(doc["data_id"])
            exchangeInfo = {}
            if 'exchangeInfo' in apply_dic[doc["data_id"]]:
                exchangeInfo = apply_dic[doc["data_id"]]['exchangeInfo']
                if 'exStatus' in exchangeInfo:
                    if exchangeInfo['exStatus'] == 'Pending':
                        exchangeInfo['exStatus']='Done'
                        apply_dic[doc["data_id"]]['exchangeInfo']=exchangeInfo
            if doc['data_status'].find('finished') != -1:
                count = count+1
                print(str(count)+'===>>>>'+str(apply_dic[doc["data_id"]]['_id']))
                print(apply_dic[doc["data_id"]]['_id'])
                data_resource_apply_collection.update_one({'_id': apply_dic[doc["data_id"]]['_id']}, {'$set': {'exchangeInfo': exchangeInfo,
                                                                                        'updated_time': doc['created_time'],
                                                                                        'status': 'finished'}})
  