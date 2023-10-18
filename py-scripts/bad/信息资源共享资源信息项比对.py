# 信息项比对结果统计脚本
# 导出csv文件到audit.zip，不需要导出的可以在main中注释
# 注意不要注释掉中间处理需要的查询结果
import csv
import datetime
import json
import os
import smtplib
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pymongo
import pymysql

env = 'DEV'
# env = 'PROD'
receivers = None
mongo_client = None
cursor = None

# 信息资源查询SQL
info_resource_sql = "select id, info_resource_name, info_resource_provider,create_date,info_resource_life_cycle, is_open, regioncode, info_item_desc_detail, share_type from cmp_catalog.info_resource_platform WHERE regioncode = '0500'"

def init_envs(env):
    if env == 'PROD':
        receivers = ['jason.lu@wingconn.com', 'tommie.chen@wingconn.com']
        mysql_conn = pymysql.connect(host="2.46.2.102", port=3306, user='bigdata', password='123@abcd',
                                     charset='utf8mb4')
        mongo_client = pymongo.MongoClient("2.46.2.239", 27017, username='admin', password='123@abcd',
                                           directConnection=True)
    else:
        receivers = ['jason.lu@wingconn.com']
        mysql_conn = pymysql.connect(host="mysql-master", port=3306, user='bigdata', password='123@abcd',
                                     charset='utf8mb4')
        mongo_client = pymongo.MongoClient(host="mongo-0.mongo,mongo-1.mongo,mongo-2.mongo`", port=27017)
        mongo_client.admin.authenticate('admin', '123@abcd', mechanism='SCRAM-SHA-1')
    # mysql 字典迭代器
    cursor = mysql_conn.cursor(cursor=pymysql.cursors.DictCursor)
    return mongo_client, cursor,receivers

# mysql查询 返回python dict array
def get_mysql_res(sql):
    resourceDict = {}
    cursor.execute(sql)
    resourceList = cursor.fetchall()
    for resource in resourceList:
        resourceDict[resource['id']] = resource
    return resourceDict

# 获取文件信息资源
def get_file_data_resource():
    fileResourceDict = {}
    dataResources = mongo_client["data_share_db"]["file_data_resource"].find({},{"info_resource_id":1,"info_items":1})
    for resource in dataResources:
        if "info_items" in resource:
            fileResourceDict[resource["info_resource_id"]] = resource["info_items"]
    return fileResourceDict

# 获取库表信息资源
def get_table_data_resource():
    tableResourceDict = {}
    dataResources = mongo_client["data_share_db"]["table_data_resource"].find({},{"info_resource_id":1,"info_items":1})
    for resource in dataResources:
        if "info_items" in resource:
            tableResourceDict[resource["info_resource_id"]] = resource["info_items"]
    return tableResourceDict

def comparison_info_items():
    resultList = []
    # 获取对比数据
    resourceDict = get_mysql_res(info_resource_sql)
    fileResourceDict = get_file_data_resource()
    tableResourceDict = get_table_data_resource()
    # 遍历信息资源
    for key, value in resourceDict.items():
        result = None
        try:
            info_item_desc_detail = json.loads(value['info_item_desc_detail'])
        except:
            print(value['info_resource_name'] + " info item detail json loads error")
        if key in fileResourceDict:
            fileItems = fileResourceDict[key]
            if len(info_item_desc_detail) != len(fileItems):
                result = value
            else:
                if not comparison_items(info_item_desc_detail, fileItems):
                    result = value
        elif key in tableResourceDict:
            tableItems = tableResourceDict[key]
            if len(info_item_desc_detail) != len(tableItems):
                result = value
            else:
                if not comparison_items(info_item_desc_detail, tableItems):
                    result = value
        # else:
        #     result = value
        if result is not None:
            result['info_resource_life_cycle'] = get_info_resource_status(result['info_resource_life_cycle'])
            resultList.append(result)
    return resultList

# 比较信息项名称是否相同
def comparison_items(source, target):
    sourceNames = ""
    targetNames = ""
    for value in source:
        sourceNames = sourceNames+value.get('infoItemName')
    for value in target:
        targetNames = targetNames+value.get('item_name')
    if sourceNames == targetNames:
        return True
    else:
        return False

# 信息资源状态转换
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
    cf.close()

def send_mail(path, receivers):
    smtp_host = 'smtp.163.com'
    port = 25
    sender = 'rikurobot@163.com'
    password = 'BDDHTVARWQRQFPFN'
    # receivers = ['jason.lu@wingconn.com', 'tommie.chen@wingconn.com', 'fisher.dai@wingconn.com']

    sub = Header('[' + env + ']'+path + '-' + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), 'utf-8')
    msg = MIMEMultipart()
    msg['Subject'] = sub
    msg['From'] = sender

    part = MIMEText('附件为'+path+'，本邮件为自动发送，请勿回复！')
    msg.attach(part)

    part = MIMEApplication(open(path, 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename=path)
    msg.attach(part)

    smtp = smtplib.SMTP(smtp_host, port, 'utf-8')
    smtp.login(sender, password)
    smtp.sendmail(sender, receivers, msg.as_string())
    smtp.quit()
    print('send msg successfully!')

if __name__ == '__main__':
    mongo_client, cursor, receivers = init_envs(env)
    print('env=' + env + ', will send to' + str(receivers))
    print('statistical task started at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    path = '信息项比对结果.csv'
    if os.path.exists(path):
        os.remove(path)
        print("remove old result")
    write_csv(comparison_info_items(), path)
    send_mail(path, receivers)
    print('statistical task completed at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))