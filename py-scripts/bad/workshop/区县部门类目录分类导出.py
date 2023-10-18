import csv
import json
import os
import datetime
from email.header import Header

from openpyxl.workbook import Workbook

import base

# env = '326'
# env = 'DEV'
env = 'DEV'
receivers = None
mongo_client = None
cursor = None
region_code = '0507'
file_context = region_code + '部门类目录分类导出'


if __name__ == '__main__':
    mongo_client, cursor, receivers, mysql_conn = base.init_envs(env)

    row_list = []
    row_list.append(["主键","目录分类名称","目录分类编码","发布标识","父目录分类名称","父目录分类编码"])
    region_map_catalog_list = base.get_mongo_res(mongo_client, "cmp_catalog", "map_catalog", {"mapCatalogCode":'0507', "mapCatalogType":'region'})
    for region_catalog in region_map_catalog_list:
        category_map_catalog_list = base.get_mongo_res(mongo_client, "cmp_catalog", "map_catalog", {"mapCatalogCode":'3', "mapCatalogParentId":str(region_catalog['_id']), "mapCatalogType":'category'})
        for category_catalog in category_map_catalog_list:
            term_map_catalog_list = base.get_mongo_res(mongo_client, "cmp_catalog", "map_catalog",
                               {"mapCatalogParentId": str(category_catalog['_id']),
                                "mapCatalogType": 'term'})
            for term_catalog in term_map_catalog_list:
                catalogue_map_catalog_list = base.get_mongo_res(mongo_client, "cmp_catalog", "map_catalog",
                                   {"mapCatalogParentId": str(term_catalog['_id']),
                                    "mapCatalogType": 'catalogue'})
                for catalogue_catalog in catalogue_map_catalog_list:
                    row_list.append([str(catalogue_catalog['_id']), catalogue_catalog['mapCatalogName'], catalogue_catalog['mapCatalogCode'], catalogue_catalog.get('publishResFlag', None), term_catalog['mapCatalogName'], term_catalog['mapCatalogCode']])




    filename = file_context + '.xlsx'
    # 创建一个工作簿
    wb = Workbook()

    # 获取活动工作表
    ws1 = wb.active
    for row in row_list:
        ws1.append(row)
    # 将所有单元格格式设置为字符串
    for row in ws1.iter_rows():
        for cell in row:
            cell.number_format = '@'

    # 将工作簿保存到 xlsx 文件
    wb.save(filename)

    ###
    sub = Header('[' + env + ']-[' + file_context + ']' + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                 'utf-8')
    base.send_mail('smtp.163.com', 25, 'rikurobot@163.com', 'BDDHTVARWQRQFPFN', ['jason.lu@wingconn.com'], sub, filename)

    # 删除文件
    os.remove(filename)
    print('export task ended at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
