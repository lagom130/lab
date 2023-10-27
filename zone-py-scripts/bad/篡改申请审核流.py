# 篡改申请流
# 当前只做了删除两条无关紧要的申请和撤销申请，更复杂的情况需要扩展该脚本
import datetime
import time

import pymongo

# 脚本执行环境
env = 'DEV'
# idiot_want_to_do属性 delete删除， 格式化日期时间字符串则为要更改成的日期时间
applies = [
    {
        'code': '202302211628526120',
        'idiot_mirages': [
            {
                'index': 0,
                'idiot_want_to_do': 'delete'
            },{
                'index': 1,
                'idiot_want_to_do': 'delete'
            }
        ]
    }
]


def init_envs(env):
    if env == 'PROD':
        mongo_client = pymongo.MongoClient("2.46.2.239", 27017, username='admin', password='123@abcd',
                                           directConnection=True)
    else:
        mongo_client = pymongo.MongoClient(host="mongo-0.mongo,mongo-1.mongo,mongo-2.mongo`", port=27017)
        mongo_client.admin.authenticate('admin', '123@abcd', mechanism='SCRAM-SHA-1')

    data_share_mongo_db = mongo_client["data_share_db"]
    data_resource_apply_collection = data_share_mongo_db["data_resource_apply"]
    operation_record_collection = data_share_mongo_db["operation_record"]
    return mongo_client, data_share_mongo_db, data_resource_apply_collection, operation_record_collection


# 判断log data status 是否为协助审核状态
def is_hand_over_log_data_status(str):
    if str == 'TABLE|handOver' or str == 'TABLE|auditApproval':
        return True
    elif str == 'FILE|handOver' or str == 'FILE|auditApproval':
        return True
    elif str == 'API|handOver' or str == 'API|auditApproval':
        return True
    else:
        return False


# 判断log data status 是否为运营审核状态
def is_admin_operate_log_data_status(str):
    if str == 'platformAudit|true' or str == 'platformAudit|false':
        return True
    else:
        return False


# 判断log data status 是否为部门最终审核状态
def is_provider_operate_log_data_status(str):
    if str == 'TABLE|auditReject' or str == 'TABLE|unSubscrib':
        return True
    elif str == 'FILE|auditReject' or str == 'FILE|unSubscrib':
        return True
    elif str == 'API|auditReject' or str == 'API|unSubscrib':
        return True
    else:
        return False


# 判断log data status 是否为撤销申请状态
def is_chexiaoshengqing_log_data_status(str):
    if str == 'TABLE|created':
        return True
    elif str == 'FILE|created':
        return True
    elif str == 'API|created':
        return True
    else:
        return False


# 判断log data status 是否为申请状态
def is_apply_operate_log_data_status(str):
    if str == 'TABLE|unAudit':
        return True
    elif str == 'FILE|unAudit':
        return True
    elif str == 'API|unAudit':
        return True
    else:
        return False


# 13位时间戳转格式化日期字符串
def timestamp_to_date_str(time_stamp, format_string="%Y-%m-%d %H:%M:%S"):
    time_array = time.localtime((time_stamp / 1000))
    str_date = time.strftime(format_string, time_array)
    return str_date


# 格式化日期字符串转13位时间戳
def date_str_to_timestamp(date_str, format_string="%Y-%m-%d %H:%M:%S"):
    t = int(time.mktime(time.strptime(date_str, format_string)))
    if len(str(t)) == 10:
        t = int(t * 1000)
    return t


# 间隔天数计算
def get_between_days_by_date_str(strat, end, format_string='%Y-%m-%d %H:%M:%S'):
    apply = datetime.datetime.strptime(strat, format_string).date()
    audit = datetime.datetime.strptime(end, format_string).date()
    delta = audit - apply
    days = delta.days + 1
    return days


# 间隔天数计算
def get_between_days_by_timestamp(strat, end):
    apply = datetime.datetime.strptime(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime((strat / 1000))),
                                       '%Y-%m-%d %H:%M:%S').date()
    audit = datetime.datetime.strptime(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime((end / 1000))),
                                       '%Y-%m-%d %H:%M:%S').date()
    delta = audit - apply
    days = delta.days + 1
    return days



# **要求的篡改审核流
def idiot_want_fake_data(the_apply):
    apply = data_resource_apply_collection.find_one({'code': the_apply['code']})
    if apply is None:
        print('[idiot want to fake data] apply cannot found, code=' + the_apply['code'])
        return
    print('[idiot want to fake data] apply [' + the_apply['code'] + '] handle')
    apply_id_str = str(apply['_id'])
    audit_depts = apply.get('audit_depts', [])
    audit_records = apply.get('audit_records', [])
    # 操作记录
    operation_records = operation_record_collection.find(
        {'data_type': 'shareResourceApply', 'data_id': apply_id_str}).sort('created_time', 1)

    logs = []
    for record in operation_records:
        logs.append(record)

    # 要篡改的数据
    idiot_mirages = the_apply['idiot_mirages']
    for idiot_mirage in idiot_mirages:
        if idiot_mirage['idiot_want_to_do'] == 'delete':
            log_data_status = logs[idiot_mirage['index']]['data_status']
            log_oid = logs[idiot_mirage['index']]['_id']
            operation_record_collection.delete_one({'_id': log_oid})
            audit_records[idiot_mirage['index']] = None
    new_audit_records = []
    for audit_record in audit_records:
        if audit_record is not None:
            new_audit_records.append(audit_record)
    data_resource_apply_collection.update_one({'_id': apply['_id']}, {'$set': {
        'audit_records': new_audit_records,
    }})


if __name__ == '__main__':
    mongo_client, data_share_mongo_db, data_resource_apply_collection, operation_record_collection = init_envs(env)
    print('[idiot want to fake data] start handle')
    for the_apply in applies:
        idiot_want_fake_data(the_apply)
    print('end')
