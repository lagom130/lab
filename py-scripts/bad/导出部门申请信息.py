# 导出部门申请信息
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

dep_name = '苏州市公安局'
file_context = dep_name + '资源申请信息'
env = 'DEV'
# env = 'PROD'
receivers = None
mongo_client = None
cursor = None

resource_type_dict = {
    'API': '接口',
    'TABLE': '库表',
    'FILE': '文件',
    'api': '接口',
    'table': '库表',
    'file': '文件',
}


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
    return mongo_client, cursor, receivers


# mongo查询 返回python dict array
def get_mongo_res(mongo_client, database, collection, query, projection=None):
    if projection is None:
        results = mongo_client[database][collection].find(query)
    else:
        results = mongo_client[database][collection].find(query, projection)
    return list(results)


# 申请状态转换
def get_apply_status(status):
    if status == 'created':
        return '已创建'
    elif status == 'unAudit':
        return '待审核'
    elif status == 'auditReject':
        return '已退回'
    elif status == 'unSubscrib':
        return '待订阅'
    elif status == 'unSend':
        return '待推送'
    elif status == 'finished':
        return '已完成'
    elif status == 'invalid':
        return '失效'
    elif status == 'handOver':
        return '转交'
    return ''


# 13位时间戳转格式化日期
def timestamp13_to_date(time_stamp, format_string="%Y-%m-%d %H:%M:%S"):
    if time_stamp is None:
        return ''
    time_array = time.localtime(time_stamp / 1000)
    str_date = time.strftime(format_string, time_array)
    return str_date


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
    print('env=' + env + ', will send to' + str(receivers))
    print('statistical task started at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    ### 查询三种资源的说明，组成resouce_id: desc的字典
    resource_desc_map = {str(item['_id']): item.get('api_desc', '') for item in
                         get_mongo_res(mongo_client, 'data_share_db', 'api_data_resource', {},
                                       {'_id': True, 'api_desc': True})}
    resource_desc_map.update({str(item['_id']): item.get('file_desc', '') for item in
                              get_mongo_res(mongo_client, 'data_share_db', 'file_data_resource', {},
                                            {'_id': True, 'file_desc': True})})
    resource_desc_map.update({str(item['_id']): item.get('table_desc', '') for item in
                              get_mongo_res(mongo_client, 'data_share_db', 'table_data_resource', {},
                                            {'_id': True, 'table_desc': True})})
    # 查询指定部门的申请
    applies = get_mongo_res(mongo_client, 'data_share_db', 'data_resource_apply', {
        "creater_dep_name": dep_name
    }, {
                                '_id': False,
                                'code': True,
                                'resource_id': True,
                                'resource_name': True,
                                'apply_type': True,
                                'status': True,
                                'business_sys_info.sys_name': True,
                                'business_sys_info.sys_ip': True,
                                'origin_incident': True,
                                'applicant_unit': True,
                                'applicant_name': True,
                                'data_creater_dep_name': True,
                                'apply_time': True,
                            })
    # 组装成行数据
    row_list = []
    # 表头
    row_list.append(['申请流水号',
                     '资源名称',
                     '资源类型',
                     '状态',
                     '资源详情-基础信息-描述',
                     '申请详情-业务系统名称',
                     '申请详情-业务系统IP',
                     '申请详情-申请使用事由',
                     '申请详情-资源使用单位名称',
                     '申请详情-使用人姓名',
                     '提供方',
                     '发起时间'
                     ])
    for apply in applies:
        resource_desc = resource_desc_map.get(apply['resource_id'], '')
        business_sys_info = apply.get('business_sys_info', {})
        sys_name = business_sys_info.get('sys_name', '')
        sys_ip = business_sys_info.get('sys_ip', '')
        row_list.append([
            apply.get('code', ''),
            apply.get('resource_name', ''),
            resource_type_dict.get(apply.get('apply_type', ''), ''),
            get_apply_status(apply.get('status', '')),
            resource_desc,
            sys_name,
            sys_ip,
            apply.get('origin_incident', ''),
            apply.get('applicant_unit', ''),
            apply.get('applicant_name', ''),
            apply.get('data_creater_dep_name', ''),
            timestamp13_to_date(apply.get('apply_time', None)),
        ])
    print('statistical task completed at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

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
