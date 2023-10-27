import datetime
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
    mongo_client = pymongo.MongoClient(
        "mongodb://admin:123%40abcd@mongo-0.mongo:27017,mongo-1.mongo:27017,mongo-2.mongo:27017/?authSource=admin")
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
    # 库表资源
    table_data_resources = mongo_db["table_data_resource"].find({}, {'_id': 1, 'table_name': 1, 'info_resource_name': 1,
                                                                     'info_resource_id': 1, 'info_items': 1})
    for data in table_data_resources:
        table_share_cache[str(data.get("_id"))] = data

    # 文件资源
    file_data_resources = mongo_db["file_data_resource"].find({}, {'_id': 1, 'file_name': 1, 'info_resource_name': 1,
                                                                   'info_resource_id': 1, 'info_items': 1})
    for data in file_data_resources:
        file_share_cache[str(data.get("_id"))] = data
    # 接口资源
    api_data_resources = mongo_db["api_data_resource"].find({}, {'_id': 1, 'api_name': 1, 'info_resource_name': 1,
                                                                 'info_resource_id': 1})
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


# 更新申请单对应的共享资源数据
def update_apply_data(apply_id, new_value):
    query = {'_id': apply_id}  # 构造查询条件
    new_value = {'$set': {'resource_name': new_value}}  # 指定要更新的字段名和新的字段值
    result = mongo_db["data_resource_apply"].update_one(query, new_value)  # 更新单个文档
    print(result)  # 输出更新的文档数，一般情况下为1


if __name__ == '__main__':
    init_share_data()
    row_list = []
    # 获取所有申请单信息
    applys = mongo_db["data_resource_apply"].find({})

    row_list = []
    row_list.append(
        ['申请流水号', '申请单id', '申请单共享资源名称', '共享资源类型', '共享资源名称'])

    index = 0
    for apply in applys:
        index += 1
        row = []

        print('进度' + '-' * 20 + ('%s ') % (index))

        apply_res_name = apply.get("resource_name")

        row.append(apply.get("code"))
        row.append(str(apply.get("_id")))
        row.append(apply_res_name)
        row.append(apply.get("apply_type"))
        # 查询共享资源
        if apply.get("resource_id") is not None:

            # 从缓存获取共享资源
            share_data_resource = None
            share_data_resource_name = None
            # 接口资源
            if apply.get("apply_type") == 'API':
                share_data_resource = api_share_cache.get(apply.get("resource_id"))
                if share_data_resource is not None:
                    share_data_resource_name = share_data_resource.get("api_name")
                else:
                    share_data_resource_name = apply_res_name
            # 文件资源
            elif apply.get("apply_type") == 'FILE':
                share_data_resource = file_share_cache.get(apply.get("resource_id"))
                if share_data_resource is not None:
                    share_data_resource_name = share_data_resource.get("file_name")
                else:
                    share_data_resource_name = apply_res_name
            # 库表资源
            else:
                share_data_resource = table_share_cache.get(apply.get("resource_id"))
                if share_data_resource is not None:
                    share_data_resource_name = share_data_resource.get("table_name")
                else:
                    share_data_resource_name = apply_res_name

            row.append(share_data_resource_name)
            # 名称不一致 需要更新
            if share_data_resource_name != apply_res_name:
                print("申请单----》", apply)
                print("共享资源----》", share_data_resource)
                row_list.append(row)
                update_apply_data(apply.get("_id"), share_data_resource_name)

    print('开始写入excel', len(row_list))
    filename = '需要更新申请单列表.xlsx'
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
    # send_mail(filename, ['leo.gao@wingconn.com'])
    print('写入excel完成')
    # os.remove(filename)
