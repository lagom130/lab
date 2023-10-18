import datetime
import os
import smtplib
import time
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pymongo
import pymysql
from openpyxl.workbook import Workbook

file_context = '信息资源统计信息'
env = '326'
# env = 'PROD'
receivers = None
mongo_client = None
cursor = None


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
    "0000": "国家级",
    "1111": "省级"
}
region_codes = ['0505','0506','0507','0508','0509','0581','0582','0583','0585','0590']


# 信息资源
info_resource_sql = "select id, info_resource_name, dept_info_resource_code, base_info_resource_code, theme_info_resource_code, info_resource_provider, info_resource_life_cycle, regioncode from cmp_catalog.info_resource_platform"

def init_envs(env):
    if env == 'PROD':
        receivers = ['jason.lu@wingconn.com', 'tommie.chen@wingconn.com', 'sisi.zhong@wingconn.com',
                     'xiao.liu@wingconn.com', 'emily.yuan@wingconn.com']

        mysql_conn = pymysql.connect(host="2.46.2.102", port=3306, user='bigdata', password='123@abcd',
                                     charset='utf8mb4')
        mongo_client = pymongo.MongoClient("2.46.2.239", 27017, username='admin', password='123@abcd',
                                           directConnection=True)
    elif env == '326':
        receivers = ['jason.lu@wingconn.com']
        mysql_conn = pymysql.connect(host="10.10.32.6", port=3306, user='wingtest', password='123@abcd',
                                     charset='utf8mb4')
        mongo_client = pymongo.MongoClient("10.10.32.6", port=27017)
        mongo_client.admin.authenticate('admin', '123@abcd', mechanism='SCRAM-SHA-1')
    else:

        receivers = ['jason.lu@wingconn.com']
        mysql_conn = pymysql.connect(host="mysql-master", port=3306, user='bigdata', password='123@abcd',
                                     charset='utf8mb4')
        mongo_client = pymongo.MongoClient(host="mongo-0.mongo,mongo-1.mongo,mongo-2.mongo`", port=27017)
        mongo_client.admin.authenticate('admin', '123@abcd', mechanism='SCRAM-SHA-1')
    # mysql 字典迭代器
    cursor = mysql_conn.cursor(cursor=pymysql.cursors.DictCursor)
    return mongo_client, cursor, receivers




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

# mongo查询 返回python dict array
def get_mongo_res(mongo_client, database, collection, query, projection=None):
    if projection is None:
        results = mongo_client[database][collection].f(query)
    else:
        results = mongo_client[database][collection].find(query, projection)
    return list(results)

### 发送邮件
def send_mail(smtp_host, port, sender, password, receivers, sub, filename):
    msg = MIMEMultipart()
    msg['Subject'] = sub
    msg['From'] = sender

    part = MIMEText('本邮件为自动发送，请勿回复！')
    msg.attach(part)

    part = MIMEApplication(open(filename, 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(part)

    smtp = smtplib.SMTP(smtp_host, port, 'utf-8')
    smtp.login(sender, password)
    smtp.sendmail(sender, receivers, msg.as_string())
    smtp.quit()
    print('send msg successfully!')

if __name__ == '__main__':
    mongo_client, cursor, receivers = init_envs(env)
    info_res_id_api_list_map = {}
    info_res_id_table_list_map = {}
    info_res_id_file_list_map = {}
    resource_published_filter = {'status':{'$in':['published', 'revokeAudit', 'revokeRejected']}}
    resource_projection = {'_id': True, 'info_resource_id': True}
    item_resources = get_mongo_res(mongo_client, 'data_share_db', 'api_data_resource', resource_published_filter,
                                   resource_projection)
    for item in item_resources:
        key = item.get('info_resource_id', '')
        res_list = info_res_id_api_list_map.get(key, [])
        res_list.append(str(item['_id']))
        info_res_id_api_list_map[key] = res_list
    item_resources = get_mongo_res(mongo_client, 'data_share_db', 'table_data_resource', resource_published_filter,
                                   resource_projection)
    for item in item_resources:
        key = item.get('info_resource_id', '')
        res_list = info_res_id_table_list_map.get(key, [])
        res_list.append(str(item['_id']))
        info_res_id_table_list_map[key] = res_list
    item_resources = get_mongo_res(mongo_client, 'data_share_db', 'file_data_resource', resource_published_filter,
                                   resource_projection)
    for item in item_resources:
        key = item.get('info_resource_id', '')
        res_list = info_res_id_file_list_map.get(key, [])
        res_list.append(str(item['_id']))
        info_res_id_file_list_map[key] = res_list

    row_list = []
    row_list.append([
        '目录名称',
        '目录发布状态',
        '共享类型',
        '提供方',
        '提供方属地',
        '目录下是否挂接资源',
        '目录下挂接资源数量',
        '目录下挂接接口资源数量',
        '目录下挂接文件资源数量',
        '目录下挂接库表资源数量',
    ])
    for regioncode in region_codes:
        data_list = get_mysql_res("select id, info_resource_name, dept_info_resource_code, base_info_resource_code, theme_info_resource_code, info_resource_provider, info_resource_life_cycle, regioncode,share_type from cmp_catalog.info_resource_platform where regioncode = '%s'" % regioncode)
        for info_resource in data_list:
            info_resource_id = str(info_resource['id'])
            file_count = len(info_res_id_file_list_map.get(info_resource_id, []))
            api_count = len(info_res_id_api_list_map.get(info_resource_id, []))
            table_count = len(info_res_id_table_list_map.get(info_resource_id, []))
            total_count = file_count + api_count + table_count
            if total_count > 0:
                has_res = '是'
            else:
                has_res = '否'

            row_list.append([
                info_resource['info_resource_name'],
                get_info_resource_status(info_resource['info_resource_life_cycle']),
                info_resource.get('share_type', ''),
                info_resource['info_resource_provider'],
                region_code_to_name_dict.get(info_resource.get('regioncode', ''), ''),
                has_res,
                total_count,
                api_count,
                file_count,
                table_count
            ])
    filename = file_context + '.xlsx'
    # 创建一个工作簿
    wb = Workbook()

    # 获取活动工作表
    ws = wb.active

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
    send_mail('smtp.163.com', 25, 'rikurobot@163.com', 'BDDHTVARWQRQFPFN', receivers, sub, filename)

    # 删除CSV文件
    os.remove(filename)
