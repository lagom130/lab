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

env = 'DEV'
# env = 'PROD'
receivers = None
mongo_client = None
mysql_conn = None
cursor = None

new_role_permission = {
                "id": "10",
                "pid": "0",
                "name": "信息资源供需管理",
                "value": "requirementMgtMenu",
                "childrens": [
                    {
                        "id": "10-1",
                        "pid": "10",
                        "name": "需求清单",
                        "value": "requirementMgtMenu-requirementListMenu",
                        "childrens": []
                    },
                    {
                        "id": "10-2",
                        "pid": "10",
                        "name": "需求受理",
                        "value": "requirementMgtMenu-requirementMenu",
                        "childrens": []
                    },
                    {
                        "id": "10-3",
                        "pid": "10",
                        "name": "督办反馈",
                        "value": "requirementMgtMenu-supervisionMenu",
                        "childrens": []
                    }
                ]
            }


def init_envs(env):
    if env == 'PROD':
        receivers = ['jason.lu@wingconn.com', 'tommie.chen@wingconn.com']
        mysql_conn = pymysql.connect(host="2.46.2.102", port=3306, user='bigdata', password='123@abcd',
                                     charset='utf8mb4')
        mongo_client = pymongo.MongoClient("2.46.2.239", 27017, username='admin', password='123@abcd',
                                           directConnection=True)
    elif env == 'UAT':
        mysql_conn = pymysql.connect(host="2.46.12.38", port=33309, user='bigdata', password='123@abcd',
                                     charset='utf8mb4')
        mongo_client = pymongo.MongoClient("2.46.12.38", 37020, username='admin', password='123@abcd',
                                           directConnection=True)
    else:

        receivers = ['jason.lu@wingconn.com']
        mysql_conn = pymysql.connect(host="mysql-master", port=3306, user='bigdata', password='123@abcd',
                                     charset='utf8mb4')
        mongo_client = pymongo.MongoClient(host="mongo-0.mongo,mongo-1.mongo,mongo-2.mongo`", port=27017)
        mongo_client.admin.authenticate('admin', '123@abcd', mechanism='SCRAM-SHA-1')
    # mysql 字典迭代器
    cursor = mysql_conn.cursor(cursor=pymysql.cursors.DictCursor)
    return mongo_client, mysql_conn, cursor, receivers


# mysql查询 返回python dict array
def get_mysql_res(sql):
    cursor.execute(sql)
    res = cursor.fetchall()
    return res


# mysql执行
def mysql_execute(sql):
    print("mysql execute : " + sql)
    cursor.execute(sql)
    res = cursor.fetchall()
    return


# 列表转字符串（sql拼接用）
def get_arr_str(arr):
    return "'" + "','".join(arr) + "'"


def get_int_arr_str(arr):
    return ",".join(map(str, arr))


# mongo查询 返回python dict array
def get_mongo_res(mongo_client, database, collection, query, projection=None):
    if projection is None:
        results = mongo_client[database][collection].find(query)
    else:
        results = mongo_client[database][collection].find(query, projection)
    return list(results)


# mongo删除
def mongo_update_by_id(mongo_client, database, collection, id, sets):
    result = mongo_client[database][collection].update_one({'_id': id}, {'$set': sets})


if __name__ == '__main__':
    print('env=' + env)
    mongo_client, mysql_conn, cursor, receivers = init_envs(env)
    role_permissions = get_mongo_res(mongo_client, 'data_share_db','role_permission', {})
    for role_permission in role_permissions:
        un_auth_perms = role_permission.get('un_auth_perms', [])
        un_auth_perms.append(new_role_permission)
        mongo_update_by_id(mongo_client, 'data_share_db','role_permission', role_permission['_id'],
                     {
                      'un_auth_perms':un_auth_perms
                     })


    print("complete!")