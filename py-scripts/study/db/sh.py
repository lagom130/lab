import re
import time
import datetime

import pymongo



if __name__ == '__main__':
    api_ids = [
        "6007fab115bac2000116ec1f",
        "6007fab115bac2000116ec1f",
        "5fffb3ef15bac2000116ea8b",
        "60014d1e15bac2000116eac4",
        "5fa8e044b29463000104ae47",
        "5fa8d945b29463000104ae42",
        "5ffec00d15bac2000116ea6e",
        "609e7450d8122900016b21a6",
        "609e7450d8122900016b21ac",
        "609e7450d8122900016b21ac",
        "609e7450d8122900016b21a6",
        "60014d1e15bac2000116eac4",
        "6007fab115bac2000116ec1f",
        "5fa8d945b29463000104ae42",
        "6136d1f72ca01400013e3c57",
        "609ca552d8122900016b2134",
        "5ec7a8c0782e8f00018bc635",
        "6246885fa43a83000144c20e",
        "5de9f6f3ddcec90001775ba1",
        "6093b010c78ed000011fac2e",
        "6079ffca7b376000013e1cca",
        "6079ffab7b376000013e1a5a",
        "6079ffde7b376000013e1e49",
        "6079ff9d7b376000013e1934",
        "6079ffdb7b376000013e1e0d",
        "6079ffc47b376000013e1c43",
        "6079ffa27b376000013e198b",
        "6079ffa37b376000013e19a6",
        "6079ff9b7b376000013e190d",
        "6079ff967b376000013e18a7",
        "6079ffd47b376000013e1d8f",
        "6079ff797b376000013e1664",
        "6079ffcc7b376000013e1cee",
        "6079ffbd7b376000013e1ba4",
        "6079ff8a7b376000013e17b4",
        "6079ffc67b376000013e1c67",
        "6079ffdd7b376000013e1e40",
        "6079ffc87b376000013e1c91",
        "6214b421d47a620001d5f4d0",
        "60f03858f1d37b00012ef507",
        "61a72b89a8e7010001f86393",
        "61a72b89a8e7010001f86399",
        "6214b421d47a620001d5f4c7",
        "6214b420d47a620001d5f4c1",
        "61a70151a8e7010001f86329",
        "61a70151a8e7010001f8632c",
        "61972142a8e7010001f85516",
        "6214b421d47a620001d5f4c4",
        "62b4181ba67a5f000180f55c",
        "62de4c7a6f1d5c00015c1556",
        "62e23bb86f1d5c00015c1891",
        "62de47cf6f1d5c00015c1549",
        "62de525a6f1d5c00015c1566",
        "62e234c56f1d5c00015c1870",
        "62de46f66f1d5c00015c1547",
        "62de4bd36f1d5c00015c1554",
        "62de48b56f1d5c00015c154b",
        "627dfd6445820e0001255610",
        "63423a815c05300001aff087",
        "63438b875c05300001aff11c",
        "6343b68d5c05300001aff128",
        "63438e705c05300001aff120",
        "63423bbf5c05300001aff08b",
        "6343bbf65c05300001aff136",
        "634e4a1b5c05300001aff3ce",
        "6343b3b05c05300001aff126",
        "6343ba2b5c05300001aff12c",
        "634e4af25c05300001aff3d0",
        "63423b365c05300001aff089",
        "6343b8785c05300001aff12a",
        "6343bb4a5c05300001aff131",
        "6343aa1a5c05300001aff124",
        "63423cd25c05300001aff08f",
        "633554925c05300001afee4f",
        "63438c485c05300001aff11e",
        "6343a8735c05300001aff122",
        "63438b875c05300001aff11c",
        "63438c485c05300001aff11e",
        "6343bb4a5c05300001aff131",
        "6343a8735c05300001aff122",
        "633554925c05300001afee4f",
        "6343b3b05c05300001aff126",
        "6343b68d5c05300001aff128",
        "63423c375c05300001aff08d",
        "634e4a1b5c05300001aff3ce",
        "6343aa1a5c05300001aff124",
        "6343ba2b5c05300001aff12c",
        "6343bbf65c05300001aff136",
        "63438e705c05300001aff120",
        "6343b8785c05300001aff12a",
        "634e4af25c05300001aff3d0",
        "637acb695c05300001b0c991",
        "62b4181ba67a5f000180f55c",
        "609ca552d8122900016b2134",
        "6246885fa43a83000144c20e",
        "63772d7a5c05300001b0c8fa",
        "63772c085c05300001b0c8f5"
    ]

    # myclient = pymongo.MongoClient("mongodb://admin:123%40abcd@2.46.2.239:27018/admin",serverSelectionTimeoutMS=1800000, socketTimeoutMS=1800000)
    # myclient = pymongo.MongoClient("mongodb://admin:123%40abcd@2.46.2.239:27018/admin")
    # myclient = pymongo.MongoClient("mongodb://admin:123%40abcd@2.46.2.239:27018/admin?readPreference=primary")
    print('query script start, please wait...')
    try:
        # myclient = pymongo.MongoClient(host="mongo-0.mongo", port=27017)
        myclient = pymongo.MongoClient("2.46.2.239", 27018,username='admin', password='123@abcd', directConnection=True)
        # myclient.admin.authenticate('admin', '123@abcd', mechanism='SCRAM-SHA-1')
        log_db = myclient["data_share_log_db"]
        col = log_db["api_log_info_old_20230328"]
        start = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('start time: ' + start)
        count = col.count_documents(filter={'apiId':{'$in':api_ids}})
        print('result is '+str(count))
        end = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('end time:' + end)
    except Exception as e:
        print('except:', e)
    finally:
        while True:
            print('query is completed, please close the window!')
            time.sleep(60)


