import csv
import json


def csv_analysis(path):
    title = []
    data_list = []
    map_dict = {}

    with open(path, encoding='utf-8') as f:
        reader = csv.reader(f)
        for row_index, row in enumerate(reader):
            if row_index is 0:
                title = row

            else:
                data = {}
                for cell_index, cell in enumerate(row):
                    key = str_to_hump(title[cell_index])
                    if cell == 'null':
                        cell = ''
                    if key == 'nettype':
                        key = 'netType'
                    elif key == 'infoItemDescDetail':
                        key = 'infoItems'
                        if cell is None or cell is '':
                            cell = '[]'
                        cell = json.loads(cell)
                        for c in cell:
                            if 'infoItemName' not in c:
                                c['infoItemName'] = ''
                            if 'dateType' not in c:
                                c['dateType'] = ''
                            if 'length' not in c or c['length'] == '':
                                c['length'] = None
                            if c['length'] is not None:
                                try:
                                    c['length'] = int(c['length'])
                                except TypeError and ValueError:
                                    c['length'] = None



                            if 'sensitiveLevel' not in c:
                                c['sensitiveLevel'] = ''
                            if 'shareType' not in c:
                                c['shareType'] = ''
                            if 'notShareReason' not in c:
                                c['notShareReason'] = ''
                            if 'isOpen' not in c:
                                c['isOpen'] = '0'
                    data[key] = cell
                    data['operationType'] = 'I'
                data_list.append(data)
    return data_list


def str_to_hump(text):
    arr = filter(None, text.lower().split('_'))
    res = ''
    for index, i in enumerate(arr):
        f = i[0].lower()
        if index is not 0:
            f = f.upper()
        res = res + f+i[1:]
    return res

if __name__ == '__main__':
    ### select id,info_resource_name,base_info_resource_code,theme_info_resource_code,dept_info_resource_code,info_resource_provider,info_resource_provider_code,info_resource_desc,info_resource_format,other_res_format_desc,info_resource_located_sys,out_res_dept,out_res_system,info_item_desc_detail,share_type,share_condition,share_mode,is_open,open_condition,update_cycle,remarks,regioncode,is_related_res_code,publish_flag,public_date,update_date,create_date,creater_id,operator,operator_id,audit_reject_reason,cancel_reject_reason,revoke_reason,info_resource_life_cycle,open_type,not_open_reason,catalog_catagory,admin_operator_name,admin_operator_id,use_scene,belong_industry,resource_subject,task_guid,task_name,gov_catalog_code,basic_catalog_code,implement_list_code,business_handling_code,nettype,certification_type,gov_use_scene,other_use_scene,field_type,other_field_type,res_registered,res_platform,org_name,org_code,approval_results,region_code,report_status,report_error_info,source_departments_text,area_code,base_one_category_code,base_two_category_code,base_multi_category_code,base_three_category_code,theme_one_category_code,theme_two_category_code,theme_multi_category_code,theme_three_category_code,dept_one_category_code,dept_two_category_code,dept_multi_category_code,dept_three_category_code from info_resource_platform
    ### 带表头
    data_list = csv_analysis("E:\\io1010\\oi.csv")
    print("start write to json")
    with open("E:\\io1010\\oiw.json", 'w', encoding='utf-8') as jf:
        jf.write(json.dumps(data_list, ensure_ascii=False, indent=2))
    print("write to json complete")
    print("write to json complete")
    with open("E:\\io1010\\oiw.csv", 'w', encoding='utf-8', newline='') as cf:
        writer = csv.writer(cf)
        for index, i in enumerate(data_list):
            for k in i.keys():
                if i[k] is None or i[k] is 'null':
                    i[k]: ''
            if index == 0:
                writer.writerow(i.keys())
            writer.writerow(i.values())
