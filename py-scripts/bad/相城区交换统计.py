import json

import pymysql

# dev
# mysql_conn = pymysql.connect(host="mysql-master", port=3306, user='bigdata', password='123@abcd', charset='utf8mb4')
# 生产
mysql_conn = pymysql.connect(host="2.46.2.102", port=3306, user='bigdata', password='123@abcd', charset='utf8mb4')
# mysql 字典迭代器
cursor = mysql_conn.cursor(cursor=pymysql.cursors.DictCursor)




# mysql查询 返回python dict array
def get_mysql_res(sql):
    cursor.execute(sql)
    res = cursor.fetchall()
    return res


if __name__ == '__main__':
    file_arr = json.load(open('E:\\file.json', "r", encoding='utf-8'))
    table_arr = json.load(open('E:\\table.json', "r", encoding='utf-8'))
    file_list = get_mysql_res("select id, resource_id from data_share_db.share_data_resource WHERE resource_type = 'FILE' and region_code = '0507'")
    table_list = get_mysql_res("select id, resource_id from data_share_db.share_data_resource WHERE resource_type = 'TABLE' and region_code = '0507'")

    file_use_count = 0
    table_use_count = 0
    for item in file_arr:
        dept_list = item['deptList']
        for dept in dept_list:
            if dept['deptNo'] == '32050700000000000':
                file_use_count = file_use_count + dept['count']
    for item in table_arr:
        dept_list = item['deptList']
        for dept in dept_list:
            if dept['deptNo'] == '32050700000000000':
                table_use_count = table_use_count + dept['count']
    print('file use='+str(file_use_count))
    print('table use='+str(table_use_count))

    file_count = 0
    table_count = 0
    for item in file_arr:
        ls_resource_id = item['resourceId']
        for res in file_list:
            if ls_resource_id == res['id'] or ls_resource_id == res['resource_id']:
                file_count += item['count']
                break
    for item in table_arr:
        ls_resource_id = item['resourceId']
        for res in table_list:
            if ls_resource_id == res['id'] or ls_resource_id == res['resource_id']:
                table_count += item['count']
                break
    print('file send =' + str(file_count))
    print('table send =' + str(table_count))

