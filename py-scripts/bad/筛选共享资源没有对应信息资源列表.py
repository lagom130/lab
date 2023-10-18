import pymongo
import pymysql
import csv

# 连接mongodb数据库-----------------------------------------------------------------------------
mongoClient = pymongo.MongoClient("mongodb://admin:123%40abcd@2.46.2.239:27017/?maxPoolSize=300")
mongoDb = mongoClient["data_share_db"]
mongoCol = mongoDb["share_data_resource"]

# 连接mysql数据库-----------------------------------------------------------------------------
mysqlConn = pymysql.connect(host="2.46.2.102", port=3306, user='bigdata', password='123@abcd', charset='utf8mb4',
                            database="cmp_catalog")
mySqlCursor = mysqlConn.cursor()


# 获取信息资源
def getInfoResCatalog(infoResourceIds):
    mySqlCursor.execute("select id from  `sn_nn`.`info_resource_platform` where id in (" + infoResourceIds + ")")
    res = mySqlCursor.fetchall()
    infoResourceIds = []
    for row in res:
        infoResourceIds.append(row[0])
    return list(infoResourceIds)


# 输出数据到csv
def outCsv(noInfoResCatalogRes):
    # 创建一个 CSV 文件并写入头部信息
    with open('筛选共享资源没有对应信息资源列表.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["共享资源名称", "创建部门名称", "对应信息资源id", "对应信息资源名称"])
        # 遍历数据，并将每行写入 CSV 文件
        for row in noInfoResCatalogRes:
            newRow = ["", "", "", ""]
            newRow[0] = row["resource_name"]
            newRow[1] = row["creater_dep_name"]
            newRow[2] = '' if row["info_resource_id"] is None else row["info_resource_id"]
            newRow[3] = '' if row["info_resource_name"] is None else row["info_resource_name"]
            print(newRow)
            writer.writerow(newRow)
            # 遍历数据，并将每行写入 CSV 文件
    # 打印输出结果
    print("Done writing data to CSV file.")


if __name__ == '__main__':
    limit = 1000
    pageSize = 1
    skip = 0

    noInfoResCatalogRes = []
    while True:
        # 获取共享资源
        shareDataResources = list(
            mongoCol.find({"creater_dep_name": {'$nin': ['测试一局', '测试二局', '测试三局']}}).limit(limit).skip(skip))
        if len(shareDataResources) == 0:
            break

        print('本次查询共享资源条数--------->', len(shareDataResources))
        # 获取共享资源绑定的信息资源id
        infoResourceIds = []
        for resource in shareDataResources:
            info_res_id_value = resource.get('info_resource_id')  # 返回 None
            if info_res_id_value is None:
                continue
            infoResourceIds.append("'" + info_res_id_value + "'")
        infoResourceIds = list(set(infoResourceIds))
        print(infoResourceIds)
        infoResourceIdsStr = ",".join(infoResourceIds)
        # 获取存在的信息资源数据
        inDbResCatalogIds = getInfoResCatalog(infoResourceIdsStr)
        for resource in shareDataResources:
            info_res_id_value = resource.get('info_resource_id')  # 返回 None
            if info_res_id_value is None:
                noInfoResCatalogRes.append(resource)
            else:
                if resource['info_resource_id'] in inDbResCatalogIds:
                    continue
                else:
                    noInfoResCatalogRes.append(resource)

        print(noInfoResCatalogRes)
        print('本次共享资源没有对应目录的条数--------->', len(noInfoResCatalogRes))
        skip = (pageSize * limit)
        pageSize += 1
        print('共查询共享资源条数--------->', skip)

    outCsv(noInfoResCatalogRes)
