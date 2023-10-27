import os
import datetime
from email.header import Header

from openpyxl.workbook import Workbook

import base



env = '326'
# env = 'DEV'
# env = 'PROD'
receivers = None
mongo_client = None
cursor = None
file_context = '已失效状态申请记录'

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
    applies = base.get_mongo_res(mongo_client, 'data_share_db', 'data_resource_apply',
                                     {'status':'invalid', 'apply_time':{'$gte':1672502400000}})
    row_list = []
    row_list.append(['申请主键', 'resourceId', 'shareResourceId', '申请流水号',
                     '申请方', '资源名称', '资源类型', '提供方', '申请状态', '申请时间','use_date_start','use_date_end','last_log_data_status','last_log_data_created_time', '历史状态记录'])
    for apply in applies:
        apply_id = str(apply.get('_id', ''))
        logs = logs_dict.get(apply_id, [])
        logs.sort(key=lambda item:datetime.datetime.strptime(item.get('created_time', ''),'%Y-%m-%d %H:%M:%S'))
        last_log = logs[-1]
        history_status = ",".join(["["+item['data_status']+": "+item['created_time']+"]" for item in logs])
        print(apply_id+": "+ str(history_status))
        row_list.append([
            str(apply['_id']),
            str(apply.get('resource_id', '')),
            str(apply.get('share_resource_id', '')),
            apply.get('code', ''),
            apply.get('dep_name', ''),
            apply.get('resource_name', ''),
            base.dict_key_to_value(base.resource_type_dict, apply.get('apply_type', ''), ''),
            apply.get('data_creater_dep_name', ''),
            base.dict_key_to_value(base.apply_status_dict,apply.get('status', ''), ''),
            base.timestamp_to_date_str(apply.get('apply_time', '')),
            apply.get('use_date_start', ''),
            apply.get('use_date_end', ''),
            last_log.get('data_status',''),
            last_log.get('created_time',''),
            history_status,
        ])

    filename = file_context + '.xlsx'
    # 创建一个工作簿
    wb = Workbook()

    # 获取活动工作表
    ws = wb.active
    ws.title = file_context
    # 将数据写入工作表
    for row in row_list:
        ws.append(row)
        print(row)
    # 将所有单元格格式设置为字符串
    for row in ws.iter_rows():
        for cell in row:
            cell.number_format = '@'

    # 将工作簿保存到 xlsx 文件
    wb.save(filename)

    ###
    sub = Header('[' + env + ']-[' + file_context + ']' + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                 'utf-8')
    base.send_mail('smtp.163.com', 25, 'rikurobot@163.com', 'BDDHTVARWQRQFPFN', receivers, sub, filename)

    # 删除文件
    os.remove(filename)
    print('export task ended at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))