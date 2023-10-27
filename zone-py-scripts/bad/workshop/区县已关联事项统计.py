import os
from datetime import datetime
from email.header import Header

from openpyxl.workbook import Workbook

import base

# env = '326'
# env = 'DEV'
env = 'PROD'
receivers = None
mongo_client = None
cursor = None
region_code = '0507'
file_context = region_code + '区县已关联事项统计'

query_region_codes = ['0505', '0506', '0507', '0508', '0509', '0581', '0582', '0583', '0585', '0590', ]

if __name__ == '__main__':
    mongo_client, cursor, receivers, mysql_conn = base.init_envs(env)
    row_title = ['事项类型', '事项名称', '部门编码', '部门名称', '属地']
    filename = file_context + '.xlsx'
    # 创建一个工作簿
    wb = Workbook()
    for query_region_code in query_region_codes:
        row_list = []
        task_list = base.get_mysql_res(cursor,"SELECT t.task_guid as task_guid, t.task_name as task_name, t.task_type as task_type, t.ou_code as ou_code, t.ou_name as ou_name, t.area_code as ou_area_code, m.dept_id, m.dept_name as dept_name FROM cmp_catalog.task t left join cmp_catalog.task_dept_map m on t.ou_code = m.ou_code where t.area_code ='32" + query_region_code + "'")
        print(query_region_code+'task size:'+str(len(task_list)))
        task_dict = {}
        for task in task_list:
            task_dict[task['task_guid']]=task
        info_res_list = base.get_mysql_res(cursor,"select id, info_resource_name, info_resource_provider,create_date,info_resource_life_cycle, is_open, regioncode, info_item_desc_detail, share_type, related_task_flag, task_guid, task_type, task_name, basic_catalog_code, business_handling_code, implement_list_code from cmp_catalog.info_resource_platform where info_resource_life_cycle in('3','4','5') and regioncode='" + query_region_code + "'")
        print(query_region_code+'info_res_list size:'+str(len(info_res_list)))
        rel_task_guid_set = set()
        for info_res in info_res_list:
            task_guid_list = list(filter(None, (info_res.get('task_guid') or "").split("|")))
            for guid in task_guid_list:
                if guid in task_dict:
                    task = task_dict[guid]
                    full_info = task['task_type']+task['task_name']+task['ou_code']+task['ou_name']+base.region_code_to_name_dict[query_region_code]
                    if full_info not in rel_task_guid_set:
                        rel_task_guid_set.add(full_info)
                        row_list.append([task['task_type'], task['task_name'], task['ou_code'], task['ou_name'],
                                         base.region_code_to_name_dict[query_region_code]])
        print(query_region_code+'rel guid set size:'+str(len(rel_task_guid_set)))

        base.write_data_to_sheet(wb.create_sheet(), base.region_code_to_name_dict[query_region_code], row_title,
                                 row_list)

    wb.save(filename)

    ###
    sub = Header('[' + env + ']-[' + file_context + ']' + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                 'utf-8')
    base.send_mail('smtp.163.com', 25, 'rikurobot@163.com', 'BDDHTVARWQRQFPFN', ['jason.lu@wingconn.com'], sub,
                   filename)

    # 删除文件
    os.remove(filename)
    print('export task ended at:' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))