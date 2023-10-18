# 共享申请记录异常
from datetime import date, timedelta, datetime

from bson import ObjectId
import pymongo


# dev
#mongo_client = pymongo.MongoClient(host="mongo-0.mongo,mongo-1.mongo,mongo-2.mongo`", port=27017)
#mongo_client.admin.authenticate('admin', '123@abcd', mechanism='SCRAM-SHA-1')
# 生产
mongo_client = pymongo.MongoClient("2.46.2.239", 27017, username='admin', password='123@abcd', directConnection=True)

data_share_db = mongo_client["data_share_db"]
operation_record_collection = data_share_db["operation_record"]
data_resource_apply_collection = data_share_db["data_resource_apply"]


if __name__ == '__main__':
    pipeline2 ={'status': {'$in': ['finished']}}
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
            if doc['data_status'].find('platformAudit|true') != -1:
                count = count+1
                print(str(count)+'===>>>>'+str(apply_dic[doc["data_id"]]['_id']))
                if apply_dic[doc["data_id"]]['apply_type'] == 'API':
                    new_doc = doc
                    new_doc.pop('_id')
                    new_doc['data_status'] = "API|finished"
                    if 'creater_dep_name' in apply_dic[doc["data_id"]]:
                        new_doc['content'] = apply_dic[doc["data_id"]]['creater_dep_name']+"已订阅"
                        new_doc['operator_name'] = apply_dic[doc["data_id"]]['creater_dep_name']
                        new_doc['operator_id'] = apply_dic[doc["data_id"]]['creater_dep_id']
                    else:
                        new_doc['content'] = "已订阅" 
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
                    data_resource_apply_collection.update_one({'_id': apply_dic[doc["data_id"]]['_id']}, {'$set': {'exchangeInfo': exchangeInfo,
                                                                                            'updated_time': new_doc['created_time'],
                                                                                            'status': 'finished'}})
                else:
                    # 订阅资源记录
                    new_doc = doc
                    new_doc.pop('_id')
                    new_doc['data_status'] = apply_dic[doc["data_id"]]['apply_type']+"|unSend"
                    if 'creater_dep_name' in apply_dic[doc["data_id"]]:
                        new_doc['content'] = apply_dic[doc["data_id"]]['creater_dep_name']+"已订阅资源"
                        new_doc['operator_name'] = apply_dic[doc["data_id"]]['creater_dep_name']
                        new_doc['operator_id'] = apply_dic[doc["data_id"]]['creater_dep_id']
                    else:
                        new_doc['content'] = "已订阅资源" 
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

                    # 推送资源记录
                    new_doc.pop('_id')
                    new_doc['data_status'] = apply_dic[doc["data_id"]]['apply_type']+"|finished"
                    if 'data_creater_dep_name' in apply_dic[doc["data_id"]]:
                        new_doc['content'] = apply_dic[doc["data_id"]]['data_creater_dep_name']+"推送资源"
                        new_doc['operator_name'] = apply_dic[doc["data_id"]]['data_creater_dep_name']
                        new_doc['operator_id'] = apply_dic[doc["data_id"]]['data_creater_dep_id']
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
                    data_resource_apply_collection.update_one({'_id': apply_dic[doc["data_id"]]['_id']}, {'$set': {'exchangeInfo': exchangeInfo,
                                                                                                   'updated_time': new_doc['created_time'],
                                                                                                    'status': 'finished'}})
        