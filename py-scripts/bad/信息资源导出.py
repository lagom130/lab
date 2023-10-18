import csv
import json

import pymongo
import pymysql

# dev
# mysql_conn = pymysql.connect(host="mysql-master", port=3306, user='bigdata', password='123@abcd', charset='utf8mb4')
# mongo_client = pymongo.MongoClient(host="mongo-0.mongo,mongo-1.mongo,mongo-2.mongo`", port=27017)
# mongo_client.admin.authenticate('admin', '123@abcd', mechanism='SCRAM-SHA-1')
# 生产
mysql_conn = pymysql.connect(host="2.46.2.102", port=3306, user='bigdata', password='123@abcd', charset='utf8mb4')
# mongo_client = pymongo.MongoClient("192.168.11.111", 27017, username='admin', password='123@abcd',
#                                    directConnection=True)
# mysql 字典迭代器
cursor = mysql_conn.cursor(cursor=pymysql.cursors.DictCursor)


region_code_to_name_dict = {
    "0500": "苏州市",
    "0505": "高新区",
    "0506": "吴中区",
    "0507": "相城区",
    "0508": "姑苏区",
    "0509": "吴江区",
    "0581": "常熟市",
    "0582": "张家港市",
    "0583": "昆山市",
    "0585": "太仓市",
    "0590": "工业园区",
}

# 区县 region map catalog code
quxian_region_map_catalog_codes = ['0582', '0581', '0585', '0583', '0509', '0506', '0507', '0508', '0590', '0505']

# 信息资源，占位符为region_code
info_resource_sql = "select id, info_resource_name, dept_info_resource_code, base_info_resource_code, theme_info_resource_code, info_resource_provider, info_resource_life_cycle, regioncode, info_item_desc_detail from cmp_catalog.info_resource_platform WHERE regioncode = '%s'"




def get_info_resource_status(status):
    if status == '0':
        return '已创建'
    elif status == '1':
        return '发布待审核'
    elif status == '2':
        return '发布已驳回'
    elif status == '3':
        return '已发布'
    elif status == '4':
        return '撤销待审核'
    elif status == '5':
        return '撤销已驳回'
    elif status == '6':
        return '已撤销'
    elif status == '7':
        return '已删除'
    return ''

# mysql查询 返回python dict array
def get_mysql_res(sql):
    cursor.execute(sql)
    res = cursor.fetchall()
    return res

# 字典数组写入csv（根据第一条数据获取属性名生成表头）
def write_csv(data_list, path):
    with open(path, 'w', encoding='utf-8', newline='') as cf:
        writer = csv.writer(cf)
        if data_list is not None:
            first_row = data_list[0]
            writer.writerow(first_row.keys())
            for i in data_list:
                for k in i.keys():
                    if i[k] is None or i[k] is 'null':
                        i[k]: ''
                writer.writerow(i.values())

if __name__ == '__main__':
    region_code = '0581'
    data_list = get_mysql_res(info_resource_sql % region_code)
    result = []
    for item in data_list:
        print(item['info_item_desc_detail'])
        info_item_names =[]
        try:
            info_item_desc_detail = json.loads(item.get('info_item_desc_detail', ''))
            for info_item in info_item_desc_detail:
                info_item_names.append(info_item.get('infoItemName'))
        except:
            print(item['info_resource_name'] + " info item detail json loads error, detail:"+str(item.get('info_item_desc_detail', '')))
        if len(info_item_names)>0:
            info_item_names_str = ''
        else:
            info_item_names_str = ','.join(info_item_names)
        result.append({
            'id': item.get('id',''),
            '名称': item.get('info_resource_name',''),
            '发布状态': get_info_resource_status(item['info_resource_life_cycle']),
            '提供方': item['info_resource_provider'],
            '提供方属地': region_code_to_name_dict.get(region_code),
            '信息项': info_item_names_str
        })
    write_csv(result, region_code_to_name_dict.get(region_code, region_code)+"目录.csv")
