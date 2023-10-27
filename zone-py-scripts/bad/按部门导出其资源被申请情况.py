import time
import csv
import pymongo

env = 'PROD'
mongo_client = None
mongo_db = None

resource_type_dict = {
    'API': '接口',
    'TABLE': '库表',
    'FILE': '文件',
    'api': '接口',
    'table': '库表',
    'file': '文件',
}


def init_envs(env):
    if env == 'PROD':
        # 连接mongodb数据库-----------------------------------------------------------------------------
        mongo_client = pymongo.MongoClient("2.46.2.239", 27017, username='admin', password='123@abcd',
                                           directConnection=True)
        mongo_db = mongo_client["data_share_db"]
    else:
        # 连接mongodb数据库-----------------------------------------------------------------------------
        mongo_client = pymongo.MongoClient("mongo-0.mongo,mongo-1.mongo,mongo-2.mongo", 27017, username='admin',
                                           password='123@abcd')
        mongo_db = mongo_client["test_xc"]

    return mongo_client, mongo_db


# 申请状态转换
def get_apply_status(status):
    if status == 'created':
        return '已创建'
    elif status == 'unAudit':
        return '待审核'
    elif status == 'auditReject':
        return '已退回'
    elif status == 'unSubscrib':
        return '待订阅'
    elif status == 'unSend':
        return '待推送'
    elif status == 'finished':
        return '已完成'
    elif status == 'invalid':
        return '失效'
    elif status == 'handOver':
        return '转交'
    return ''


# 13位时间戳转格式化日期
def timestamp13_to_date(time_stamp, format_string="%Y-%m-%d %H:%M:%S"):
    if time_stamp is None:
        return ''
    time_array = time.localtime(time_stamp / 1000)
    str_date = time.strftime(format_string, time_array)
    return str_date


if __name__ == '__main__':
    dep_name = '苏州市市场监督管理局'
    mongo_client, mongo_db = init_envs(env)
    applies = mongo_db['data_resource_apply'].find({"data_creater_dep_name": dep_name})
    apis = list(mongo_db['api_data_resource'].find({"creater_dep_name": dep_name}, {'_id': True, 'api_name': True}))
    tables = list(
        mongo_db['table_data_resource'].find({"creater_dep_name": dep_name}, {'_id': True, 'table_name': True}))
    files = list(mongo_db['file_data_resource'].find({"creater_dep_name": dep_name}, {'_id': True, 'file_name': True}))

    share_data_res = {}
    for api in apis:
        share_data_res[str(api['_id'])] = api['api_name']
    for table in tables:
        share_data_res[str(table['_id'])] = table['table_name']
    for file in files:
        share_data_res[str(file['_id'])] = file['file_name']
    # 创建一个 CSV 文件并写入头部信息
    with open('【共享】按部门导出其资源被申请情况.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['申请方',
                         '共享资源名称',
                         '共享资源类型',
                         '提供方',
                         '申请状态',
                         '申请理由',
                         '发起申请时间',
                         '提供方审核时间'
                         ])
        # 遍历数据，并将每行写入 CSV 文件
        for apply in applies:
            row_list = [
                apply.get('dep_name', ''),
                share_data_res.get(apply['resource_id'], ''),
                resource_type_dict.get(apply.get('apply_type', ''), ''),
                apply.get("data_creater_dep_name", ""),
                get_apply_status(apply.get('status', '')),
                apply.get('origin_incident', ''),
                timestamp13_to_date(apply.get('apply_time', None)),
                timestamp13_to_date(apply.get('provider_audit_time', None)),
            ]
            print(row_list)
            writer.writerow(row_list)
        # 打印输出结果
    print("Done writing data to CSV file.")
