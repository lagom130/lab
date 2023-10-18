import re
import time
import datetime

import pymongo



if __name__ == '__main__':
    # 1675070040000
    # 1675070160000

    # myclient = pymongo.MongoClient("mongodb://admin:123%40abcd@2.46.2.239:27018/admin",serverSelectionTimeoutMS=1800000, socketTimeoutMS=1800000)
    # myclient = pymongo.MongoClient("mongodb://admin:123%40abcd@2.46.2.239:27018/admin")
    # myclient = pymongo.MongoClient("mongodb://admin:123%40abcd@2.46.2.239:27018/admin?readPreference=primary")
    print('query script start, please wait...')
    try:
        # myclient = pymongo.MongoClient(host="mongo-0.mongo", port=27017)
        myclient = pymongo.MongoClient("2.46.2.239", 27018,username='admin', password='123@abcd', directConnection=True)
        # myclient.admin.authenticate('admin', '123@abcd', mechanism='SCRAM-SHA-1')
        log_db = myclient["comm_logstore"]
        col = log_db["BigData.APIGateway"]
        records = col.find({'logType':'SERVICE_LOG', 'createdTime':{'$gte':1675070040000, '$lte': 1675070160000}, 'content':re.compile('5ffd4983e8761b000109988b')})
        for record in records:
            print(record)
    except Exception as e:
        print('except:', e)



