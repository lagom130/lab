import pymysql

# 连接mysql数据库-----------------------------------------------------------------------------

mysqlConn = pymysql.connect(host="2.46.2.102",
                            port=3306,
                            user='bigdata',
                            password='123@abcd',
                            charset='utf8mb4',
                            database="cmp_catalog")
mySqlCursor = mysqlConn.cursor()


# 数据格式化
def formatData(value):
    return '' if value is None else value


key = '%s_%s'
# 加载所有task到内存中
taskCache = {}


# 加载所有task到内存中
def initTaskData():
    mySqlCursor.execute(
        "select  `task_guid`, `task_type`, `task_name`, `basic_catalog_code`, `business_handling_code`, `implement_list_code`, `dept_id`, `ou_code`, `ou_name`, `area_code` from task")
    res = list(mySqlCursor.fetchall())
    for data in res:
        # 主键 = task_name+ '_' + ou_code
        keyItem = key % (str(data[2]).strip(), str(data[7]).strip())
        taskCache[keyItem] = data


# 查询task_name不为空，task_guid为空的信息资源
getInfoResSql = "select  `id`, `task_name`,`org_code` from info_resource_platform where `task_guid` is null and  `task_name` is not null and  `task_name` !='' "
# 更新task_name不为空，task_guid为空的信息资源
updateSql = "UPDATE `info_resource_platform` SET task_guid = %s, task_type=%s, basic_catalog_code=%s, business_handling_code=%s WHERE `id` = %s;"

# 没有task对应信息的信息资源id
noTaskGuidInfoResIds = set()
# 已处理信息资源数
handleDataCount = 0


# 处理信息资源
def handleInfoResCatalog(handleDataCount):
    while True:
        try:
            getInfoResSqlItem = getInfoResSql
            if len(noTaskGuidInfoResIds) != 0:
                getInfoResSqlItem += (
                        " and `id` not in (%s)" % ("'" + "', '".join(str(x) for x in noTaskGuidInfoResIds) + "'"))
            getInfoResSqlItem += " order by `id` limit 1000 "
            mySqlCursor.execute(getInfoResSqlItem)
            infoResourceList = list(mySqlCursor.fetchall())
            # 不存在数据，结束循环
            if len(infoResourceList) == 0:
                break
            # 本次循环需要更新的数据集合
            update_values = [];
            for infoResource in infoResourceList:
                # 初始化需要更新的数据
                taskGuidArr = []
                taskTypeArr = []
                basicCatalogCodeArr = []
                businessHandlingCodeArr = []
                # 信息资源中多个任务名称切分
                infoResTaskNameArr = infoResource[1].split("|")
                for infoResTaskName in infoResTaskNameArr:
                    # 主键 = task_name+ '_' + org_code
                    keyItem = key % (str(infoResTaskName).strip(), str(infoResource[2]).strip())
                    # print("****", keyItem)
                    # 从缓存中获取对应的task信息
                    task = taskCache.get(keyItem, None)
                    # print("----", task)
                    if task is None:
                        continue
                    else:
                        taskGuidArr.append(formatData(task[0]))
                        taskTypeArr.append(formatData(task[1]))
                        basicCatalogCodeArr.append(formatData(task[3]))
                        businessHandlingCodeArr.append(formatData(task[4]))

                if len(taskGuidArr) > 0:
                    # 添加需要更新的数据集合
                    update_values.append(('|'.join(taskGuidArr),
                                          '|'.join(taskTypeArr),
                                          '|'.join(basicCatalogCodeArr),
                                          '|'.join(businessHandlingCodeArr),
                                          infoResource[0]))
                    print("处理的信息资源id--- >", infoResource[0])
                    handleDataCount += 1
                else:
                    noTaskGuidInfoResIds.add(infoResource[0])
            # 使用游标对象的 executemany() 方法批量更新数据
            mySqlCursor.executemany(updateSql, update_values)
            # 提交所有更改并关闭数据库连接
            mysqlConn.commit()

        except BaseException as e:
            print(e)
            break
    print("未在task表中找到对应数据的总数--- >", len(noTaskGuidInfoResIds))
    print("已处理数据总数--- >", handleDataCount)
    mySqlCursor.close()
    mysqlConn.close()


if __name__ == '__main__':
    # 加载所有task到内存中
    initTaskData()
    # 更新信息资源相关数据
    handleInfoResCatalog(handleDataCount)
