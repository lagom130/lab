import datetime
import json
import os

import pymongo
import pymysql
from openpyxl import Workbook
import smtplib
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

'''
根据申请记录，查询共享资源以及库表类资源其绑定的信息资源信息项信息
'''

env = 'dev'
mongo_db = None
mySqlCursor = None

# 连接mongodb数据库-----------------------------------------------------------------------------
if env == 'PROD':
    # 连接mongodb数据库-----------------------------------------------------------------------------
    mongo_client = pymongo.MongoClient("2.46.2.239", 27017, username='admin', password='123@abcd',
                                       directConnection=True)
    mongo_db = mongo_client["data_share_db"]
    # 连接mysql数据库-----------------------------------------------------------------------------
    mysqlConn = pymysql.connect(host="2.46.2.102", port=3306, user='bigdata', password='123@abcd', charset='utf8mb4',
                                database="cmp_catalog")
    mySqlCursor = mysqlConn.cursor()
else:
    # 连接mongodb数据库-----------------------------------------------------------------------------
    mongo_client = pymongo.MongoClient("mongo-0.mongo", 27017, username='admin',
                                       password='123@abcd',
                                       directConnection=True)
    mongo_db = mongo_client["test_xc"]

    # 连接mysql数据库-----------------------------------------------------------------------------
    mysqlConn = pymysql.connect(host="10.10.32.6", port=3306, user='wingtest', password='123@abcd', charset='utf8mb4',
                                database="sn_nn")
    mySqlCursor = mysqlConn.cursor()

catalog_cache = {}

table_share_cache = {}

file_share_cache = {}

api_share_cache = {}


# 从mysql加载所有信息资源到内存中
def init_catalog_data():
    mySqlCursor.execute(
        "select `id`, `info_item_desc_detail` from info_resource_platform ")
    res = list(mySqlCursor.fetchall())
    for data in res:
        catalog_cache[data[0]] = data[1]


# 从mongodb加载所有共享资源到内存中
def init_share_data():
    table_data_resources = mongo_db["table_data_resource"].find({})
    for data in table_data_resources:
        table_share_cache[str(data.get("_id"))] = data
    file_data_resources = mongo_db["file_data_resource"].find({})
    for data in file_data_resources:
        file_share_cache[str(data.get("_id"))] = data
    api_data_resources = mongo_db["api_data_resource"].find({})
    for data in api_data_resources:
        api_share_cache[str(data.get("_id"))] = data


# 发送邮件
def send_mail(path, receivers):
    smtp_host = 'smtp.163.com'
    port = 25
    sender = 'rikurobot@163.com'
    password = 'BDDHTVARWQRQFPFN'
    # receivers = ['jason.lu@wingconn.com', 'tommie.chen@wingconn.com', 'fisher.dai@wingconn.com']

    sub = Header('[' + env + ']' + path + '-' + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), 'utf-8')
    msg = MIMEMultipart()
    msg['Subject'] = sub
    msg['From'] = sender

    part = MIMEText('附件为' + path + '，本邮件为自动发送，请勿回复！')
    msg.attach(part)

    part = MIMEApplication(open(path, 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename=path)
    msg.attach(part)

    smtp = smtplib.SMTP(smtp_host, port, 'utf-8')
    smtp.login(sender, password)
    smtp.sendmail(sender, receivers, msg.as_string())
    smtp.quit()
    print('send msg successfully!')


# 申请单状态
status = {
    'created': '已创建',
    'unAudit': '待审核',
    'auditReject': '审核已退回',
    'unSubscrib': '已同意/待订阅',
    'unSend': '已订阅/待推送',
    'finished': '已推送/已完成',
    'invalid': '已失效',
    'handOver': '已转交'
}

if __name__ == '__main__':
    init_catalog_data()
    init_share_data()
    row_list = []
    row_list.append(['申请方', '共享资源名称', '共享资源类型', '所属目录', '提供方', '审核状态', '信息项名称', '数据格式', '长度'])
    # 获取所有申请单信息
    applys = mongo_db["data_resource_apply"].find({}).sort("updated_time", pymongo.DESCENDING)
    index = 0
    for apply in applys:

        row = []
        row.append(apply.get("creater_dep_name"))
        row.append(apply.get("resource_name"))
        row.append(apply.get("apply_type"))
        row.append('')
        row.append(apply.get("data_creater_dep_name"))
        row.append(status.get(apply.get("status")))
        # 查询共享资源
        if apply.get("resource_id") is not None:
            # 从缓存获取共享资源
            share_data_resource = None
            if apply.get("apply_type") == 'API':
                share_data_resource = api_share_cache.get(apply.get("resource_id"))
            elif apply.get("apply_type") == 'FILE':
                share_data_resource = file_share_cache.get(apply.get("resource_id"))
            else:
                share_data_resource = table_share_cache.get(apply.get("resource_id"))

            # 共享资源不为空
            if share_data_resource is not None:
                # 所属目录
                row[3] = share_data_resource.get("info_resource_name")
                # 库表资源需要再查询信息资源
                if share_data_resource.get("info_resource_id") is not None:
                    items = catalog_cache.get(share_data_resource.get("info_resource_id"), '')
                    # 信息资源的信息项
                    if items is not None and len(items) > 0:
                        items = json.loads(catalog_cache[share_data_resource.get("info_resource_id")])
                        first = False
                        if items is not None:
                            for item in items:
                                # 多个信息项
                                if first:
                                    row = []
                                    row.append("")
                                    row.append("")
                                    row.append("")
                                    row.append("")
                                    row.append("")
                                    row.append("")
                                else:
                                    first = True
                                row.append(item.get('infoItemName', ''))
                                row.append(item.get('dateType', ''))
                                row.append(item.get('length', ''))
                                row_list.append(row)
                else:
                    row_list.append(row)
            else:
                row_list.append(row)
        index += 1
        print('进度' + '-' * 20 + ('%s ') % (index))

    print('开始写入excel')
    filename = '【共享】根据申请记录，查询共享资源以及信息资源的信息项信息.xlsx'
    # 创建一个工作簿
    wb = Workbook()
    # 获取活动工作表
    ws = wb.active
    # 将数据写入工作表
    for row in row_list:
        ws.append(row)
    # 将所有单元格格式设置为字符串
    for row in ws.iter_rows():
        for cell in row:
            cell.number_format = '@'
    # 将工作簿保存到 xlsx 文件
    wb.save(filename)
    send_mail(filename, ['leo.gao@wingconn.com', 'jason.lu@wingconn.com'])
    print('写入excel完成')
    os.remove(filename)
