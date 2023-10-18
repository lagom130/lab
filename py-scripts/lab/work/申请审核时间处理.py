# 审核时间处理脚本，需搭配datashare-svc的数据处理接口使用，具体使用方式查看main方法
import datetime
import time

import pymongo

# 创建时间、运营审核时间、部门审核时间过滤条件
limit_time = '2022-09-01 00:00:00'
# 运营审核时长过滤条件
limit_admin_length = 2
# 部门审核时长过滤条件
limit_provider_length = 10
# 修改运营审核时长
change_admin_length = 1
# 修改部门审核时长
change_provider_length = 5

ONEDAY_TIMESTAMP = 86400000

# dev
# mongo_client = pymongo.MongoClient(host="mongo-0.mongo,mongo-1.mongo,mongo-2.mongo`", port=27017)
# mongo_client.admin.authenticate('admin', '123@abcd', mechanism='SCRAM-SHA-1')
# 生产

mongo_client = pymongo.MongoClient("192.168.11.111", 27017, username='admin', password='123@abcd',
                                   directConnection=True)

# mongo 库
data_share_mongo_db = mongo_client["data_share_db"]
# ds mongo 集合
data_resource_apply_collection = data_share_mongo_db["data_resource_apply"]
operation_record_collection = data_share_mongo_db["operation_record"]


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


# 获取申请操作记录
def get_apply_operation_records():
    logs_dict = {}
    operation_records = operation_record_collection.find({'data_type': 'shareResourceApply'}).sort('created_time', 1)
    for record in operation_records:
        item_records = logs_dict.get(record['data_id'], [])
        item_records.append(record)
        logs_dict[record['data_id']] = item_records
    return logs_dict


# 运营审核时间处理
def apply_admin_handle(logs_dict):
    applies = data_resource_apply_collection.find(
        {'$and': [{'apply_time': {'$exists': 1}},
                  {'$or': [{'created_time': {'$gte': limit_time}},
                           {'admin_audit_time': {'$gte': date_str_to_timestamp(limit_time)}},
                           {'provider_audit_time': {'$gte': date_str_to_timestamp(limit_time)}}]}]}).sort(
        'created_time', 1)
    for apply in applies:
        apply_id = str(apply['_id'])
        audit_depts = apply.get('audit_depts', [])
        audit_records = apply.get('audit_records', [])
        logs = logs_dict.get(apply_id, [])
        old_admin_audit_time_length = apply.get('admin_audit_time_length', None)
        old_admin_audit_time = apply.get('admin_audit_time', None)
        apply_time = apply.get('apply_time')
        if old_admin_audit_time_length is None:
            continue
        admin_used_ms = old_admin_audit_time - apply_time
        if admin_used_ms > (limit_admin_length * ONEDAY_TIMESTAMP):
            admin_used_day_mod_ms = admin_used_ms % ONEDAY_TIMESTAMP
            target_admin_audit_timestamp = int(
                (((change_admin_length - 1) * ONEDAY_TIMESTAMP) + admin_used_day_mod_ms) + apply_time)
            target_admin_audit_time = timestamp_to_date_str(target_admin_audit_timestamp)
            changed_log_id = None
            print('apply=' + timestamp_to_date_str(apply_time) + ",old_audit=" + timestamp_to_date_str(
                old_admin_audit_time) + ",target=" + target_admin_audit_time)
            last_apply_log_timestamp = None
            for log in logs:
                if is_apply_operate_log_data_status(log['data_status']):
                    last_apply_log_timestamp = date_str_to_timestamp(log['created_time'])
                if is_admin_operate_log_data_status(log['data_status']):
                    changed_log_id = log['_id']
            if changed_log_id is not None:
                operation_record_collection.update_one({'_id': changed_log_id},
                                                       {'$set': {'created_time': target_admin_audit_time}})
            for audit_dept in audit_depts:
                if audit_dept['dept_id'] == 'admin':
                    audit_dept['audit_time'] = target_admin_audit_time
            for audit_record in audit_records:
                source_audit_timestamp = date_str_to_timestamp(audit_record['audit_time'])
                if last_apply_log_timestamp < source_audit_timestamp:
                    if audit_record['dep_code'] == 'admin':
                        audit_record['audit_time'] = target_admin_audit_time

            data_resource_apply_collection.update_one({'_id': apply['_id']},
                                                      {'$set': {'audit_depts': audit_depts,
                                                                'audit_records': audit_records}})


# 部门审核时间处理
def apply_provider_handle(logs_dict):
    applies = data_resource_apply_collection.find(
        {'$and': [{'admin_audit_time': {'$exists': 1}},
                  {'$or': [{'created_time': {'$gte': limit_time}},
                           {'admin_audit_time': {'$gte': date_str_to_timestamp(limit_time)}},
                           {'provider_audit_time': {'$gte': date_str_to_timestamp(limit_time)}}]}]}).sort(
        'created_time', 1)
    for apply in applies:
        apply_id = str(apply['_id'])
        audit_records = apply.get('audit_records', [])
        audit_depts = apply.get('audit_depts', [])
        logs = logs_dict.get(apply_id, [])
        admin_audit_time = apply.get('admin_audit_time', None)
        old_provider_audit_time = apply.get('provider_audit_time', None)
        if old_provider_audit_time is None:
            continue
        audit_used_ms = old_provider_audit_time - admin_audit_time
        if audit_used_ms > (limit_provider_length * ONEDAY_TIMESTAMP):
            audit_used_day_mod_ms = int(audit_used_ms % ONEDAY_TIMESTAMP)
            target_provider_audit_timestamp = int(
                (((change_provider_length - 1) * ONEDAY_TIMESTAMP) + audit_used_day_mod_ms) + admin_audit_time)
            target_provider_audit_time = timestamp_to_date_str(target_provider_audit_timestamp)
            print('admin audit=' + timestamp_to_date_str(admin_audit_time) + ",old_audit=" + timestamp_to_date_str(
                old_provider_audit_time) + ",target=" + target_provider_audit_time)
            last_apply_log_timestamp = None
            for log in logs:
                if is_apply_operate_log_data_status(log['data_status']):
                    last_apply_log_timestamp = date_str_to_timestamp(log['created_time'])
            # 部门中间审核时间处理
            coor_logs = []
            for log in logs:
                if date_str_to_timestamp(
                        log['created_time']) > last_apply_log_timestamp and is_hand_over_log_data_status(
                    log['data_status']):
                    coor_logs.append(log)
            coor_logs_len = len(coor_logs)
            for coor_log_index, coor_log in enumerate(coor_logs):
                # 运营申请时间与部门最终审核时间按中间审核数量切分，修改中间审核时间
                coor_log['created_time'] = timestamp_to_date_str(
                    admin_audit_time + int((target_provider_audit_timestamp - admin_audit_time) // (coor_logs_len + 1)))
                operation_record_collection.update_one({'_id': coor_log['_id']},
                                                       {'$set': {'created_time': coor_log['created_time']}})
            for log in logs:
                if is_provider_operate_log_data_status(log['data_status']) and date_str_to_timestamp(
                        log['created_time']) > last_apply_log_timestamp:
                    log['created_time'] = target_provider_audit_time
                    operation_record_collection.update_one({'_id': log['_id']},
                                                           {'$set': {'created_time': target_provider_audit_time}})
                    coor_logs.append(log)
            for audit_dept in audit_depts:
                for coor_log in coor_logs:
                    if audit_dept['dept_name'] == coor_log['operator_name']:
                        audit_dept['audit_time'] = coor_log['created_time']

            for audit_record in audit_records:
                source_audit_timestamp = date_str_to_timestamp(audit_record['audit_time'])
                if last_apply_log_timestamp < source_audit_timestamp:
                    for coor_log in coor_logs:
                        if audit_record['dep_name'] == coor_log['operator_name']:
                            audit_record['audit_time'] = coor_log['created_time']
            data_resource_apply_collection.update_one({'_id': apply['_id']},
                                                      {'$set': {'audit_depts': audit_depts,
                                                                'audit_records': audit_records}})


# 先注释掉step2，执行step1，接口调用完成后再注释掉step1，执行step2
if __name__ == '__main__':
    # step1. 处理部门审核时间，完成后调用接口
    # 先处理运营审核时间，然后调用接口生成审核数据
    # print('start process admin audit  at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # logs_dict = get_apply_operation_records()
    # apply_admin_handle(logs_dict)
    print('admin process, please request api!')
    print('curl --request GET --url http://localhost:8350/dataProcess/applies/auditTime')

    # step2. 处理部门审核时间，完成后调用接口
    # 再处理部门审核时间，然后调用接口生成审核数据
    print('start process provider audit  at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    logs_dict = get_apply_operation_records()
    apply_provider_handle(logs_dict)
    print('provider process, please request api!')
    print('curl --request GET --url http://localhost:8350/dataProcess/applies/auditTime')
    print('end process at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print('end')
