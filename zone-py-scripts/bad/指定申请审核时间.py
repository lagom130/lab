# 修改申请的运营审核时间和提供方审核时间到指定值
import datetime
import time

import pymongo

# 脚本执行环境
env = 'DEV'
# {code:xxxx, admin_time:'2022:xx:xx xx:xx:xx', 'provider_time':'2022-9-16 16:17:00'}  、
applies = [
    {'code': '202209131624363256', 'admin_time': '2022-09-15 11:20:00', 'provider_time': '2022-9-16 16:17:00'},
    {'code': '202210241541517704', 'admin_time': '2022-10-25 11:26:00', 'provider_time': '2022-10-27 17:54:00'},
    {'code': '202210241549076199', 'admin_time': '2022-10-25 11:28:00', 'provider_time': '2022-10-27 17:54:00'},
    {'code': '202210241553371801', 'admin_time': '2022-10-25 11:28:00', 'provider_time': '2022-10-27 17:55:00'},
    {'code': '202302091042301480', 'admin_time': '2023-02-12 10:21:00', 'provider_time': '2023-02-20 09:47:00'},
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


# 处理运营方审核时间
def handle_apply_admin(the_apply):
    apply = data_resource_apply_collection.find_one({'code': the_apply['code']})
    if apply is None:
        print('[admin_time_handle] apply cannot found, code=' + the_apply['code'])
        return
    if apply['[admin_time_handle] admin_audit_time'] is not None and timestamp_to_date_str(apply['admin_audit_time']) == \
            the_apply[
                'admin_time']:
        print(
            ('[admin_time_handle] apply [' + the_apply['code'] + '] target admin audit time is equals source, skip it'))
        return
    print('[admin_time_handle] apply [' + the_apply['code'] + '] handle admin audit time')
    apply_id_str = str(apply['_id'])
    target_admin_audit_time = the_apply['admin_time']
    target_admin_audit_timestamp = date_str_to_timestamp(the_apply['admin_time'])
    apply_time = apply.get('apply_time', '')
    old_admin_audit_time = apply.get('admin_audit_time', None)
    print('apply=' + timestamp_to_date_str(apply_time) + ",old_admin_audit=" + timestamp_to_date_str(
        old_admin_audit_time) + ",target=" + target_admin_audit_time)

    audit_depts = apply.get('audit_depts', [])
    audit_records = apply.get('audit_records', [])
    # 操作记录
    operation_records = operation_record_collection.find(
        {'data_type': 'shareResourceApply', 'data_id': apply_id_str}).sort('created_time', 1)

    logs = []
    for record in operation_records:
        logs.append(record)

    # 运营审核时间处理
    changed_log_id = None
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
    if apply['provider_audit_time'] is None:
        data_resource_apply_collection.update_one({'_id': apply['_id']}, {'$set': {
            'audit_depts': audit_depts,
            'audit_records': audit_records,
            'admin_audit_time': target_admin_audit_timestamp,
            'admin_audit_time_length': get_between_days_by_timestamp(apply['apply_time'], target_admin_audit_timestamp),
        }})
    else:
        data_resource_apply_collection.update_one({'_id': apply['_id']}, {'$set': {
            'audit_depts': audit_depts,
            'audit_records': audit_records,
            'admin_audit_time': target_admin_audit_timestamp,
            'admin_audit_time_length': get_between_days_by_timestamp(apply['apply_time'], target_admin_audit_timestamp),
            'provider_audit_time_length': get_between_days_by_timestamp(target_admin_audit_timestamp,
                                                                        apply['provider_audit_time']),
        }})


# 处理提供方审核时间
def handle_apply_provider(the_apply):
    apply = data_resource_apply_collection.find_one({'code': the_apply['code']})
    if apply is None:
        print('[provider_time_handle] apply cannot found, code=' + the_apply['code'])
        return
    if apply['provider_audit_time'] is not None and timestamp_to_date_str(apply['provider_audit_time']) == the_apply[
        'provider_time']:
        print(('[provider_time_handle] apply [' + the_apply[
            'code'] + '] target provider audit time is equals source, skip it'))
        return
    print('[provider_time_handle] apply [' + the_apply['code'] + '] handle provider audit time')
    apply_id_str = str(apply['_id'])
    target_provider_audit_time = the_apply['provider_time']
    target_provider_audit_timestamp = date_str_to_timestamp(the_apply['provider_time'])
    admin_audit_time = apply.get('admin_audit_time', None)
    old_provider_audit_time = apply.get('provider_audit_time', None)
    print(
        '[provider_time_handle] admin_audit_time=' + timestamp_to_date_str(
            admin_audit_time) + ",old_provider_audit=" + timestamp_to_date_str(
            old_provider_audit_time) + ",target=" + target_provider_audit_time)

    audit_depts = apply.get('audit_depts', [])
    audit_records = apply.get('audit_records', [])
    # 操作记录
    operation_records = operation_record_collection.find(
        {'data_type': 'shareResourceApply', 'data_id': apply_id_str}).sort('created_time', 1)

    logs = []
    for record in operation_records:
        logs.append(record)

    # 提供方审核时间处理
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
            admin_audit_time + int((target_provider_audit_timestamp - admin_audit_time) // (coor_logs_len + 1)) * (
                        coor_log_index + 1))
        print('[provider_time_handle] apply[' + the_apply['code'] + '] change overHander time, coor_log_id=' + str(
            coor_log['_id']) + '. change time to ' + coor_log['created_time'])
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
    data_resource_apply_collection.update_one({'_id': apply['_id']}, {'$set': {
        'audit_depts': audit_depts,
        'audit_records': audit_records,
        'provider_audit_time': target_provider_audit_timestamp,
        'provider_audit_time_length': get_between_days_by_timestamp(admin_audit_time, target_provider_audit_timestamp),
    }})


if __name__ == '__main__':
    mongo_client, data_share_mongo_db, data_resource_apply_collection, operation_record_collection = init_envs(env)
    print('[admin_time_handle] start handle admin audit time')
    for the_apply in applies:
        admin_time = the_apply.get('admin_time', None)
        if admin_time is not None and admin_time != '':
            handle_apply_admin(the_apply)
        else:
            print('[admin_time_handle] apply[' + the_apply['code'] + '] target admin audit time is empty, so skip it')
    print('[provider_time_handle] start handle provider audit time')
    for the_apply in applies:
        provider_time = the_apply.get('provider_time', None)
        if provider_time is not None and provider_time != '':
            handle_apply_provider(the_apply)
        else:
            print('[provider_time_handle] apply[' + the_apply[
                'code'] + '] target provider audit time is empty, so skip it')
    print('end')
