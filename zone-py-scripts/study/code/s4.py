import csv
import json



def csv_analysis(path):
    title = []
    data_list = []

    with open(path, encoding='utf-8') as f:
        reader = csv.reader(f)
        for row_index, row in enumerate(reader):
            if row_index is 0:
                title = row

            else:
                data = {}
                for index, i in enumerate(row):
                    data[title[index]] = i
                data_list.append(data)
    return data_list



def sub_step(status):
    if status == 'unSend' :
        return 1
    elif status == 'finished':
        return 1
    else:
        return 0

def write_csv(data_list, path):
    with open(path, 'w', encoding='utf-8', newline='') as cf:
        writer = csv.writer(cf)
        for index, i in enumerate(data_list):
            for k in i.keys():
                if i[k] is None or i[k] is 'null':
                    i[k]: ''
            if index == 0:
                writer.writerow(i.keys())
            writer.writerow(i.values())

if __name__ == '__main__':
    sbwy_list = csv_analysis("E:\\io721\\sbwy.csv")
    apply_simple_list = csv_analysis("E:\\io721\\as.csv")
    info_resource_2_sys_list = csv_analysis("E:\\io721\\iid2sys.csv")
    sd_2_ir_id_list = csv_analysis("E:\\io721\\sd2iid.csv")
    record_list = csv_analysis("E:\\io721\\record.csv")


    iid_sys_map = {}
    for item in info_resource_2_sys_list:
        iid_sys_map[item['id']] = item.get('info_resource_located_sys', '')

    rid_sys_map = {}
    for item in sd_2_ir_id_list:
        rid_sys_map[item['resource_id']] = iid_sys_map.get(item['info_resource_id'], '无')

    record_map = {}
    for item in record_list:
        if item['data_type'] == 'shareResourceApply':
            rs = record_map.get(item['data_id'], [])
            rs.append(item)
            record_map[item['data_id']] = rs


    data_list = []
    for item in sbwy_list:

        for apply in apply_simple_list:
            if apply['resource_id'] == item['resource_id'] or apply['share_resource_id'] == item['resource_id']:
                audit = ''
                if apply['status'] == 'auditReject':
                    audit = '驳回'
                elif apply['status'] == 'unSubscrib':
                    audit = '同意'
                elif apply['status'] == 'unSend':
                    audit = '同意'
                elif apply['status'] == 'finished':
                    audit = '同意'
                elif apply['revoke_status'] == 'REVOKED':
                    audit = '撤销'
                else:
                    audit = apply['status']
                records = record_map.get(apply['_id'], [])
                apply['applyTime'] = ''
                apply['adminAuditTime'] = ''
                apply['deptAuditTime'] = ''
                for r in records:
                    if apply['applyTime'] =='' and (r['data_status'] == 'API|unAudit' or r['data_status'] == 'TABLE|unAudit' or r['data_status'] == 'FILE|unAudit'):
                        apply['applyTime']= r['created_time']
                    elif r['data_status'] == 'platformAudit|true' or r['data_status'] == 'API|unSubscrib' or r['data_status'] == 'TABLE|unSubscrib' or r['data_status'] == 'FILE|unSubscrib':
                        if apply['adminAuditTime'] == '' and (r['operator_id'] == 'admin' or r['operator_id'] == '0'):
                            apply['adminAuditTime'] = r['created_time']
                        elif apply['deptAuditTime'] == '':
                            apply['deptAuditTime']= r['created_time']

                data = {
                    '填表范围（市本级、县区名称）': item['region_name'],
                    '行政区划名称（如：盐城市）': item['region_name'],
                    '单位名称': item['creater_dep_name'],
                    '数据资源目录名称': item['info_resource_name'],
                    '来源系统名称': rid_sys_map.get(item['resource_id'], '无'),
                    '申请单位名称': apply['creater_dep_name'],
                    '申请业务系统': apply['business_sys_info.sys_name'],
                    '审核意见（如：通过，驳回）': audit,
                    '申请时间': apply['applyTime'],
                    '平台审核时间': apply['adminAuditTime'],
                    '审核时间': apply['deptAuditTime'],
                }
                data_list.append(data)



    write_csv(data_list, 'E:\\io721\\sheet4new2.csv')
    print('over')

