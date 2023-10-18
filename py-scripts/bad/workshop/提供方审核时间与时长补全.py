import os
import datetime

import base



file_context = '一件事相关申请单'
# env = '326'
env = 'DEV'
# env = 'PROD'
receivers = None
mongo_client = None
cursor = None


def get_logs_dict():
    logs_dict = dict()
    operation_records = base.get_mongo_res(mongo_client, 'data_share_db', 'operation_record',
                       {'data_type': 'shareResourceApply'})
    for log in operation_records:
        key = log.get('data_id', '')
        if key == '':
            continue
        logs = logs_dict.get(key, [])
        logs.append(log)
        logs_dict[key] = logs
    return logs_dict


def update_provider_audit_time(apply, provider_audit_time):
    base.mongo_update_by_id(mongo_client, 'data_share_db', 'data_resource_apply', apply['_id'], {'provider_audit_time': provider_audit_time})



if __name__ == '__main__':
    mongo_client, cursor, receivers = base.init_envs(env)
    logs_dict = get_logs_dict()
    api_applies = base.get_mongo_res(mongo_client, 'data_share_db', 'data_resource_apply',
                                     {'apply_type':'API','status':'finished', 'provider_audit_time': None})
    for apply in api_applies:
        logs = logs_dict.get(str(apply['_id']), [])
        log = None
        for item in logs:
            if item.get('data_status','') == 'API|unSubscrib':
                log = item
                break
            if item.get('data_status','') == 'API|finished':
                log = item
                break
        if log is not None:
            provider_audit_time = base.convert_to_timestamp(log['created_time'])
            update_provider_audit_time(apply, provider_audit_time)
        else:
            print(apply['apply_type']+':'+apply['code'] + " cannot convert")
    table_applies = base.get_mongo_res(mongo_client, 'data_share_db', 'data_resource_apply',
                                     {'apply_type': 'TABLE', 'status': {'$in':['unSend','finished']}, 'provider_audit_time': None})
    for apply in table_applies:
        logs = logs_dict.get(str(apply['_id']), [])
        log = None
        for item in logs:
            if item.get('data_status','') == 'TABLE|unSubscrib':
                log = item
                break
            if item.get('data_status','') == 'TABLE|unSend':
                log = item
                break
        if log is not None:
            provider_audit_time = base.convert_to_timestamp(log['created_time'])
            update_provider_audit_time(apply, provider_audit_time)
        else:
            print(apply['apply_type']+':'+apply['code'] + " cannot convert")
    file_applies = base.get_mongo_res(mongo_client, 'data_share_db', 'data_resource_apply',
                                       {'apply_type': 'FILE', 'status': {'$in': ['unSend', 'finished']},
                                        'provider_audit_time': None})
    for apply in file_applies:
        logs = logs_dict.get(str(apply['_id']), [])
        log = None
        for item in logs:
            if item.get('data_status', '') == 'FILE|unSubscrib':
                log = item
                break
            if item.get('data_status', '') == 'FILE|unSend':
                log = item
                break
        if log is not None:
            provider_audit_time = base.convert_to_timestamp(log['created_time'])
            update_provider_audit_time(apply, provider_audit_time)
        else:
            print(apply['apply_type']+':'+apply['code'] + " cannot convert")
    print(str(len(api_applies)))
    print(str(len(table_applies)))
    print(str(len(file_applies)))
    print('export task ended at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))