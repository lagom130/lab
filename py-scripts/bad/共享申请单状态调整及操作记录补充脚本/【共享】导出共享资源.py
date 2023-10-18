import datetime
import os

import pymongo
import pymysql
from openpyxl import Workbook
import smtplib
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

env = 'PROD'
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
        "select `id`, `info_resource_name`,  `share_type`,  `is_open`, `open_type`,`regioncode` from info_resource_platform  WHERE 	regioncode IN ( '0500', '0505', '0506', '0507', '0508', '0509', '0581', '0582', '0583', '0585', '0590' )  ")
    res = list(mySqlCursor.fetchall())
    for data in res:
        catalog_cache[data[0]] = data


# 从mysql加载所有信息资源到内存中
intuu = 0
def init_catalog_data1(id):
    global intuu
    mySqlCursor.execute((
                            "select `id`, `info_resource_name`,  `share_type`,  `is_open`, `open_type`,`regioncode` from info_resource_platform  WHERE  id = '%s' ") % (
                            id))
    res = list(mySqlCursor.fetchall())
    if len(res) > 0:
        intuu += 1
        print(intuu)
        return res[0]
    else:
        return None


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


# 状态
status = {
    'created': '已创建',
    'publishAudit': '发布待审核',
    'published': '已发布',
    'publishRejected': '发布已驳回',
    'revokeAudit': '撤销待审核',
    'revoked': '已撤销',
    'revokeRejected': '撤销已驳回',
    'closed': '已关闭'

}

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
    "0590": "工业园区"
}


def get_info_res(res_id):
    if res_id is not None:
        info_res = catalog_cache.get(res_id)
        if info_res is None:
            info_res = ["", "", "", "", "", ""]
        res = [info_res[1], info_res[2],
               '是' if '1' == info_res[3] else '否']
        if info_res[4] == 'conditional':
            res.append("有条件开放")
        elif info_res[4] == 'disallowed':
            res.append("不开放")
        else:
            res.append("")
        res.append(region_code_to_name_dict.get(info_res[5], ""))
        return res
    else:
        print("未找到信息资源--》" + res_id)
        return None


def build_data(field, data, res, type):
    row = []
    row.append(data.get(field, ""))
    row.append(type)
    row.append(data.get("creater_dep_name", ""))
    row.append("" if res is None else res[4])
    row.append(status.get(data.get("status", ""), ""))
    row.append(data.get("created_time", ""))
    row.append(data.get("share_range", ""))
    row.append("" if res is None else res[0])
    row.append("" if res is None else res[1])
    row.append("" if res is None else res[2])
    row.append("" if res is None else res[3])
    return row

if __name__ == '__main__':
    init_catalog_data()
    init_share_data()
    row_list = []
    row_list.append(
        ['信息资源名称', '信息资源类型', '提供方', '提供方属地', '信息资源状态', '发布时间', '信息资源共享类型', '所属信息资源目录', '所属信息资源目录共享类型', '所属信息资源目录是否开放',
         '所属信息资源目录开放类型'
         ])
    index = 0
    for table in table_share_cache.values():
        if table.get("related_catalog_info") is None or table.get("related_catalog_info").get("region_code") not in region_code_to_name_dict.keys():
            continue
        index += 1
        print("table------>" + str(index))
        res = get_info_res(table.get("info_resource_id"))
        if res is None:
            continue
        row = build_data("table_name", table, res, "TABLE")
        if len(row[3]) ==0:
            row[3] = table.get("related_catalog_info").get("region_name")
        row_list.append(row)
    index = 0
    for file in file_share_cache.values():
        if file.get("related_catalog_info") is None or file.get("related_catalog_info").get("region_code") not in region_code_to_name_dict.keys():
            continue
        index += 1
        print("file------>" + str(index))
        res = get_info_res(file.get("info_resource_id"))
        if res is None:
            continue
        row = build_data("file_name", file, res, "FILE")
        if len(row[3]) ==0:
            row[3] = file.get("related_catalog_info").get("region_name")
        row_list.append(row)
    index = 0
    for api in api_share_cache.values():
        if api.get("related_catalog_info") is None or api.get("related_catalog_info").get("region_code") not in region_code_to_name_dict.keys():
            continue
        index += 1
        print("api------>" + str(index))
        res = get_info_res(api.get("info_resource_id"))
        if res is None:
            continue
        row = build_data("api_name", api, res, "API")
        if len(row[3]) ==0:
            row[3] = api.get("related_catalog_info").get("region_name")
        row_list.append(row)

    print('开始写入excel', len(row_list))
    filename = '市区县共享资源列表.xlsx'
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
    send_mail(filename, ['leo.gao@wingconn.com'])
    print('写入excel完成')
    os.remove(filename)
