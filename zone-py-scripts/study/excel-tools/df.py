import csv
import json
import os
import csv
import time


status_dict = {"created":"已创建","releaseWaitingApproval": "发布待审核", "revoked": "已撤销", "released": "已发布", "releaseAlreadyReturn": "发布被驳回","expired": "已失效", "DELETE": "已删除"}



def csv_analysis_to_dict(path):
    dept_dict = {}
    with open(path, encoding='utf-8') as f:
        reader = csv.reader(f)
        for row_index, row in enumerate(reader):
            if row_index != 0:
                dept_dict[row[0]] = row[1]
    return dept_dict


def json_analysis_to_dict(path):
    json_fp = open(path, "r", encoding='utf-8')
    return json.load(json_fp)


def dict_write_to_csv(data_list, path):
    with open(path, 'w', encoding='utf-8', newline='') as cf:
        writer = csv.writer(cf)
        for index, i in enumerate(data_list):
            for k in i.keys():
                if i[k] is None or i[k] is 'null':
                    i[k]: ''
            if index == 0:
                writer.writerow(i.keys())
            writer.writerow(i.values())


def timestamp_convert(timestamp, sdf):
    if timestamp == '':
        return ''
    i = int(timestamp)/1000
    t = time.localtime(i)
    return time.strftime(sdf, t)


if __name__ == '__main__':
    dop_label_dict = json_analysis_to_dict("E:\\dopdata\\dop_label_info.json")
    dept_dict = csv_analysis_to_dict("E:\\dopdata\\org_department.csv")
    dop_resources_meta_dict = json_analysis_to_dict("E:\\dopdata\\dop_resources_meta.json")

    file_id_dept_name_map={}
    file_id_filename_map={}
    res_list=[]
    for r in dop_resources_meta_dict:

        basic_info = r['basicInfo']
        categories = basic_info.get('categories', [])
        cvs = ''
        if len(categories) > 0:
           c = categories[0]
           for l in dop_label_dict:
               if l['level'] == c['level'] and l['_id']['$oid'] == c['id']:
                   cvs = l['name']


        technical_info = r['technicalInfo']
        name = basic_info['resourceName']
        dept_id = basic_info['deptId']
        dept_name = dept_dict.get(dept_id, '未知部门')
        file_list = technical_info.get('fileList', [])
        output_file_list =[]
        for fi in file_list:

            output_file_list.append({
                "fileName": fi['fileName'],
                "downloadUrl": fi['fileDownloadAddress'],
                "publicTime": timestamp_convert(fi['createDate'], '%Y-%m-%d %H:%M:%S')
            })
            file_id_dept_name_map[fi['id']] = dept_name
            file_id_filename_map[fi['id']] = fi['fileName']
        res_item = {
            '创建局办': dept_name,
            '资源名称': name,
            '所属目录资源名称': basic_info['resourceDirectory'],
            '所属分类': cvs,
            '更新周期': basic_info['updateFrequency'],
            '发布时间': timestamp_convert(basic_info['updateDate']['$numberLong'], '%Y-%m-%d %H:%M:%S'),
            '更新时间': timestamp_convert(basic_info.get('releaseDate', {}).get('$numberLong', ''), '%Y-%m-%d %H:%M:%S'),
            '数据状态': status_dict.get(basic_info['resourceStatus'], basic_info['resourceStatus']),
            '数据描述': basic_info['abstract'],
            '上传文件信息': output_file_list,
        }
        res_list.append(res_item)
    dict_write_to_csv(res_list, "E:\\dopdata\\output.csv")
    with open("E:\\dopdata\\file_id_dept_name_map.json", 'w', encoding='utf-8') as f:
        f.write(json.dumps(file_id_dept_name_map, ensure_ascii=False, indent=2))
    with open("E:\\dopdata\\file_id_filename_map.json", 'w', encoding='utf-8') as f2:
        f2.write(json.dumps(file_id_filename_map, ensure_ascii=False, indent=2))
    print('end!')