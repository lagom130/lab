import re
import time
import datetime

import pymongo



if __name__ == '__main__':
    dept_id = '815527129549747438'

    # myclient = pymongo.MongoClient("mongodb://admin:123%40abcd@2.46.2.239:27018/admin",serverSelectionTimeoutMS=1800000, socketTimeoutMS=1800000)
    # myclient = pymongo.MongoClient("mongodb://admin:123%40abcd@2.46.2.239:27018/admin")
    # myclient = pymongo.MongoClient("mongodb://admin:123%40abcd@2.46.2.239:27018/admin?readPreference=primary")
    print('query script start, please wait...')
    try:
        query = {'applicantId':dept_id}
        # myclient = pymongo.MongoClient(host="mongo-0.mongo", port=27017)
        myclient = pymongo.MongoClient("2.46.2.239", 27018,username='admin', password='123@abcd', directConnection=True)
        # myclient.admin.authenticate('admin', '123@abcd', mechanism='SCRAM-SHA-1')
        log_db = myclient["data_share_log_db"]
        col_1 = log_db["api_log_info"]
        col_2 = log_db["api_log_info_old"]
        col_3 = log_db["api_log_info_old_20230328"]
        start = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('start time: ' + start)
        count_1 = col_1.count_documents(filter=query)
        print('api_log_info result is '+str(count_1))
        end = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('end time:' + end)
        print('start time: ' + start)
        count_2 = col_2.count_documents(filter=query)
        print('api_log_info_old result is ' + str(count_2))
        end = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('end time:' + end)
        print('start time: ' + start)
        count_3 = col_3.count_documents(filter=query)
        print('api_log_info_old_20230328 result is ' + str(count_3))
        end = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('end time:' + end)
        print('api_log_info result is ' + str(count_1))
        print('api_log_info_old result is ' + str(count_2))
        print('api_log_info_old_20230328 result is ' + str(count_3))
        print(('total='+str(int(count_1)+int(count_2)+int(count_3))))

    except Exception as e:
        print('except:', e)


