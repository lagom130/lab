# 如果控制台输出curl语句，去cmp_catalogmgt_service容器中手动执行
import datetime
import json

import base


region_code='0505'
info_resource_life_cycle = '3'
info_resource_names = ['重大科技成果', '孵化企业总表','院所基本信息']
# env = '326'
# env = 'DEV'
env = 'PROD'
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

    mongo_client, cursor, receivers, mysql_conn = base.init_envs(env)

    info_resources = base.get_mysql_res(cursor, "select * from cmp_catalog.info_resource_platform where regioncode='%s' and info_resource_life_cycle ='%s' and info_resource_name in (%s)" % (region_code, info_resource_life_cycle, base.get_arr_str(info_resource_names)))
    for info_res in info_resources:
        info_res_id = info_res['id']
        logs = base.get_mongo_res(mongo_client, 'cmp_catalog', 'infoResOPLogEntity', {'infoResourceId': info_res_id})
        logs.sort(key=lambda item: datetime.datetime.strptime(item.get('createTime', ''), '%Y-%m-%d %H:%M:%S'))
        want_delete_log = logs[-1]
        target_status_log = logs[-2]
        want_delete_log_oid = want_delete_log['_id']
        target_info_res_value = target_status_log['infoResNewValue']
        target_info_res = json.loads(target_info_res_value)
        info_resource_life_cycle = target_info_res.get('infoResourceLifeCycle','')
        is_open = target_info_res.get('isOpen','')
        if is_open == '1':
            print(info_res['info_resource_name'] + " 是开放的，需要手动处理curl --request GET --url 'http://localhost:8310/kafkaMsg/infoResource/sendModify/" + info_res['id']+"'")
        base.mongo_delete_by_id(mongo_client, 'cmp_catalog', 'infoResOPLogEntity' , want_delete_log_oid)
        cursor.execute("update cmp_catalog.info_resource_platform set info_resource_life_cycle = '"+info_resource_life_cycle+"' where id='"+info_res_id+"'")
        if info_resource_life_cycle == '3':
            cursor.execute("update cmp_catalog.info_resource_platform set public_date = Null where id='" + info_res_id + "'")
        mysql_conn.commit()


    print('export task ended at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))