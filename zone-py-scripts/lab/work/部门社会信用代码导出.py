# 导出部门名称与社会信用代码在data share中的存储
# 导出csv文件到同级文件夹
import datetime
import time

import pymongo
import csv


# dev
mongo_client = pymongo.MongoClient(host="mongo-0.mongo,mongo-1.mongo,mongo-2.mongo`", port=27017)
mongo_client.admin.authenticate('admin', '123@abcd', mechanism='SCRAM-SHA-1')
# 生产
# mongo_client = pymongo.MongoClient("192.168.11.111", 27017, username='admin', password='123@abcd',
#                                    directConnection=True)


cmp_catalog_mongo_db = mongo_client["cmp_catalog"]
org_region_map_collection = cmp_catalog_mongo_db["org_region_map"]

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
    print('export to csv started at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    data_list = []
    # 过滤不需要的字段
    region_maps = org_region_map_collection.find({}, {"orgName": 1, "orgCode":1, "regionName":1, "regionCode":1, "_id":0})
    write_csv(region_maps, "部门机构代码.csv")
    print('export to csv completed at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
