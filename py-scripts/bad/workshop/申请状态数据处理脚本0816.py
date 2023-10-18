import os
import datetime
from email.header import Header

from bson import ObjectId
from openpyxl.workbook import Workbook

import base



# env = '326'
env = 'DEV'
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


if __name__ == '__main__':
    mongo_client, cursor, receivers,mysql_conn = base.init_envs(env)
    logs_dict = get_logs_dict()
    applies = base.get_mongo_res(mongo_client, 'data_share_db', 'data_resource_apply',
                                     {'status':{'$in':['unAudit','auditReject','invalid']}})
    to_un_platform_audit = 0
    to_platform_reject = 0
    invalid_to_true = 0
    invalid_apply_list = []
    for apply in applies:
        #1. 待审核处理, 运营未审核，修改为待审核（运营）unPlatormAudit,否则就是部门待审核，保持unAudit
        if apply.get('status','') == 'unAudit':
            if apply.get('admin_audit_time', None) is None or apply.get('is_platform_audit', "false") == "true":
                to_un_platform_audit = to_un_platform_audit + 1
                base.mongo_update_by_id(mongo_client, 'data_share_db', 'data_resource_apply', apply['_id'],
                                        {'status': 'unPlatformAudit'})
        #2. 审核未通过，根据审核时间判断，如果有提供方审核时间，就是auditReject，如果没有,就是platformAuditReject
        elif apply.get('status','') == 'auditReject':
            if apply.get('provider_audit_time', None) is None:
                to_platform_reject = to_platform_reject + 1
                base.mongo_update_by_id(mongo_client, 'data_share_db', 'data_resource_apply', apply['_id'],
                                        {'status': 'platformAuditReject'})
        #3. 已失效，要将invalid设置为true, 并导出列表，由人工去判断reasonType和status
        elif apply.get('status','') == 'invalid':
            auto_invalid_type = False
            invalid_to_true = invalid_to_true + 1
            base.mongo_update_by_id(mongo_client, 'data_share_db', 'data_resource_apply', apply['_id'],
                                    {'invalid': True})
            if auto_invalid_type == False and apply.get('revoke_status','') == 'REVOKED':
                auto_invalid_type = True
                # base.mongo_update_by_id(mongo_client, 'data_share_db', 'data_resource_apply', apply['_id'],
                #                         {'invalid_type': 3})
            if auto_invalid_type == False:
                try:
                    use_date_end = datetime.datetime.strptime(apply.get('use_date_end', ''), '%Y-%m-%d')
                    if use_date_end < datetime.datetime.today():
                        auto_invalid_type = True
                        base.mongo_update_by_id(mongo_client, 'data_share_db', 'data_resource_apply', apply['_id'],
                                                {'invalid_type': 1})
                except ValueError:
                    print("格式不正确，后续手动处理")

            if auto_invalid_type == False :
                    resource_id = apply.get('resource_id','')
                    resource_type = apply.get('apply_type')
                    collection = ''
                    if resource_type == 'API':
                        collection = 'api_data_resource'
                    elif resource_type == 'TABLE':
                        collection = 'table_data_resource'
                    elif resource_type == 'FILE':
                        collection = 'file_data_resource'
                    resource = base.get_one_mongo_res(mongo_client, 'data_share_db', collection,
                                               {'_id': ObjectId(resource_id)})
                    if resource is not None and resource.get('status', '') not in ['published','revokeAudit','revokeRejected']:
                        auto_invalid_type = True
                        base.mongo_update_by_id(mongo_client, 'data_share_db', 'data_resource_apply', apply['_id'],
                                                {'invalid_type': 2})
            # 未处理失效原因或者23年的申请数据，需要手动处理失效原因和状态
            if auto_invalid_type == False or apply.get('apply_time',0)>1672502400000:
                apply['invalid_type_need_fill'] = auto_invalid_type is False
                invalid_apply_list.append(apply)

    row_list = []
    row_list.append(['是否需要改status','是否需要改invalid_type','申请主键', 'resourceId', 'shareResourceId', '申请流水号',
                     '申请方', '资源名称', '资源类型', '提供方', '申请状态', '申请时间','use_date_start','use_date_end','last_log_data_status','last_log_data_created_time', '历史状态记录'])
    for apply in invalid_apply_list:
        apply_id = str(apply.get('_id', ''))
        logs = logs_dict.get(apply_id, [])
        # logs.sort(key=lambda item:datetime.datetime.strptime(item.get('created_time', ''),'%Y-%m-%d %H:%M:%S'))
        if len(logs) == 0 :
            last_log = {}
            history_status = ''
        else:
            last_log = logs[-1]
            history_status = ",".join(["["+item['data_status']+": "+str(item['created_time'])+"]" for item in logs])
        print(apply_id+": "+ str(history_status))
        if apply.get('apply_time',0)>1672502400000 and apply['invalid_type_need_fill'] is False and last_log.get('data_status','') in ['API|finished','TABLE|finished','FILE|finished']:
            print(apply_id + ": " + str(history_status))
            base.mongo_update_by_id(mongo_client, 'data_share_db', 'data_resource_apply', apply['_id'],
                                    {'status': 'finished'})
        else:
            row_list.append([
                str(apply.get('apply_time',0)>1672502400000),
                str(apply['invalid_type_need_fill']),
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
    if env == 'PROD':
        smtp_host = 'mail.xxzx.suzhou.gov.cn'
        sender = 'superdop@xxzx.suzhou.gov.cn'
        passowrd = 'suzhou@12kfpt'
    else:
        smtp_host = 'smtp.163.com'
        sender = 'rikurobot@163.com'
        passowrd = 'BDDHTVARWQRQFPFN'
    base.send_mail(smtp_host, 25, sender, passowrd, ['jason.lu@wingconn.com'], sub, filename)

    # 删除文件
    os.remove(filename)
    print('to_un_platform_audit = '+str(to_un_platform_audit))
    print('to_platform_reject = '+str(to_platform_reject))
    print('invalid_to_true = '+str(invalid_to_true))
    print('export task ended at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))