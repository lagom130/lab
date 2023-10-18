# 需共享平台提供的统计数据 过滤掉省级数据
import csv
import datetime
import gc
import itertools
import json
import os
import smtplib
import time
import zipfile
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pymongo
import pymysql

file_context = '需共享平台提供的统计数据'
# env = '326'
# env = 'DEV'
env = 'PROD'
receivers = None
mongo_client = None
cursor = None

#########################################################################################################
######## 字典 ###########################################################################################
# 属地字典
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
city_region = '0500'
area_regions = ['0505', '0506', '0507', '0508', '0509', '0581', '0582', '0583', '0585', '0590']
province_regions = ['0000', '1111']
filter_info_resource_code_prefix = '30701505003030050000000003'
# 目录分类（按行业）
belong_industry_dict = {
    "A": "农、林、牧、渔业",
    "B": "采矿业",
    "C": "制造业",
    "D": "电力、势力、燃气及水生产和供应业",
    "E": "建筑业",
    "F": "批发和零售业",
    "G": "交通运输、仓储和邮政业",
    "H": "住宿和餐饮业",
    "I": "信息传输、软件和信息技术服务业",
    "J": "金融业",
    "K": "房地产业",
    "L": "租赁和商务服务业",
    "M": "科学研究和技术服务业",
    "N": "水利、环境和公共设施管理业",
    "O": "居民服务、修理和其他服务业",
    "P": "教育",
    "Q": "卫生和社会工作",
    "R": "文化、体育和娱乐业",
    "S": "公共管理、社会保障和社会组织",
    "T": "国际组织"
}
# 布尔中文-字符串01
bool_number_string_dict = {
    "1": "是",
    "0": "否"
}
# 是否电子证照
certification_type_dict = {
    "1": "是",
    "2": "否"
}
# 事项目录所属领域
field_type_dict = {
    "1": "科技创新",
    "2": "商贸流通",
    "3": "社会救助",
    "4": "城建住房",
    "5": "教育文化",
    "6": "工业农业",
    "7": "机构团体",
    "8": "地理空间",
    "9": "资源能源",
    "10": "市场监管",
    "11": "生活服务",
    "12": "生态环境",
    "13": "交通运输",
    "14": "安全生产",
    "15": "社保就业",
    "16": "医疗卫生",
    "17": "信用服务",
    "18": "公共服务",
    "19": "财税金融",
    "20": "气象服务",
    "21": "法律服务",
    "22": "新冠疫苗",
    "23": "其他"
}
# 应用场景
gov_use_scene_dict = {
    "1": "政务服务",
    "2": "公共服务",
    "3": "监管",
    "0": "其他"
}
# 目录生命周期
info_res_life_cycle_dict = {
    "0": "已创建",
    "1": "发布待审核",
    "2": "发布已驳回",
    "3": "已发布",
    "4": "撤销待审核",
    "5": "撤销已驳回",
    "6": "已撤销",
    "7": "已删除"
}
# 信息项共享类型
item_share_type_dict = {
    "1": "无条件共享",
    "2": "有条件共享",
    "3": "不予共享"
}
# 提供渠道
net_type_dict = {
    "1": "政务外网",
    "2": "互联网",
    "3": "部门专网"
}
# 开放类型
open_type_dict = {
    "unconditional": "无条件开放",
    "conditional": "有条件开放",
    "disallowed": "不开放"
}
# 不xx依据
reason_type_dict = {
    1: "法律法规",
    2: "政策文件",
    3: "涉及敏感信息",
    4: "其他"
}
# 所属领域
resource_subject_dict = {
    "01": "婚育收养",
    "02": "环境资源",
    "03": "教育培训",
    "04": "住房保障",
    "05": "劳动就业",
    "06": "执业资格",
    "07": "社会保障",
    "08": "纳税缴费",
    "09": "医疗卫生",
    "10": "交通旅游",
    "11": "出境入境",
    "12": "生活服务",
    "13": "民族宗教",
    "14": "三农服务",
    "15": "死亡殡葬",
    "16": "设立变更",
    "17": "行业准营",
    "18": "投资立项",
    "19": "工程建设",
    "20": "涉外服务",
    "21": "安全生产",
    "22": "破产注销",
    "23": "文物保护",
    "24": "其他"
}
# 数据敏感级别
sensitive_level_dict = {
    "1": "1级",
    "2": "2级",
    "3": "3级",
    "4": "4级"
}
# 存储类型
storage_mode_dict = {
    "API": "接口",
    "TABLE": "数据库",
    "FILE_STRUCTURED": "结构化文件",
    "FILE_UNSTRUCTURED": "非结构化文件"
}
# 事项类型
task_type_dict = {
    "GOV": "政务服务事项",
    "PUBLIC": "公共服务事项"
}
# 目录分类（按主题）
use_scene_dict = {
    "01": "社会保险",
    "02": "交通出行",
    "03": "婚育",
    "04": "社区周边生活服务",
    "05": "政府办事",
    "06": "就医与保健",
    "07": "学校教育与终身教育",
    "08": "培训与就业",
    "09": "城市安全"
}
# 布尔值字典
bool_dict = {
    True: '是',
    False: '否'
}
# 布尔值字符串字典
bool_str_dict = {
    'true': '是',
    'false': '否'
}
# 布尔值字符串字典
bool_yn_dict = {
    'Y': '是',
    'N': '否'
}
# 更新周期
update_cycle_dict = {
    'year': '每年',
    'quarter': '季度',
    'month': '每月',
    'week': '每周',
    'day': '每日',
    'ondemand': '按需',
    '实时': '实时',
    '每日': '每日',
    '每周': '每周',
    '每月': '每月',
    '季度': '季度',
    '每年': '每年',
    '按需': '按需'
}

# 资源状态
data_res_status_dict = {
    'created': '已创建',
    'publishAudit': '发布待审核',
    'published': '已发布',
    'publishRejected': '发布已驳回',
    'revokeAudit': '撤销待审核',
    'revoked': '已撤销',
    'revokeRejected': '撤销已驳回',
    'closed': '已关闭',
}
# 匹配模式
url_map_mode_dict = {
    'prefix': '前缀匹配',
    'absolute': '绝对匹配',
}
# 请求类型
api_protocol_dict = {
    'rs': 'restful',
    'ws': 'webservice'
}
# 资源类型
resource_type_dict = {
    'API': '接口',
    'TABLE': '库表',
    'FILE': '文件',
    'api': '接口',
    'table': '库表',
    'file': '文件',
}
# 申请状态
apply_status_dict = {
    'created': '已创建',
    'unAudit': '待审核',
    'auditReject': '已退回',
    'unSubscrib': '待订阅',
    'unSend': '待推送',
    'finished': '已完成',
    'invalid': '失效',
    'handOver': '转交'
}
# 省级上报状态
report_status_dict = {
    None: '未发布',
    '': '未发布',
    'handled': '已绑定',
    'initializing': '初始化中',
    'initialized': '初始化完成',
    'migrating': '迁移中',
    'migrated': '迁移完成',
    'published': '已发布',
    'unpublished': '不发布'}
# 目录省级上报状态
info_resource_report_status_dict = {
    None: '未上报',
    '': '未上报',
    'success': '已上报'
}

###########################################################################################################
######## 通用方法 ###########################################################################################

# 根据字典key获取字典值，缺省默认值为空字符串
def dict_key_to_value(dictionary, key, default_value=""):
    return dictionary.get(key, default_value)


# 根据字典值获取字典key，缺省默认值为空字符串
def dict_value_to_key(dictionary, value, default_value=""):
    for k, v in dictionary.items():
        if v == value:
            return k
    return default_value


def get_element(arr, i, default_value=""):
    try:
        return arr[i]
    except IndexError:
        return default_value


# 单一实体占用多行写入单元格，只有第一行会写
def write_cell(entity_index, value):
    if entity_index == 0:
        return value
    return None


# 单一实体占用多行写入单元格，只有第一行会写，并将值翻译
def write_cell_convert_by_dict(entity_index, dictionary, key, default_value=""):
    if entity_index == 0:
        return dict_key_to_value(dictionary, key, default_value)
    return None


# 单一实体占用多行写入单元格，只有第一行会写
def entity_to_cell(entity_index, entity, key):
    if entity_index == 0:
        return entity.get(key, None)
    return None


# 单一实体占用多行写入单元格，只有第一行会写，并将值翻译
def entity_to_cell_convert_by_dict(entity_index, dictionary, entity, key, default_value=""):
    if entity_index == 0:
        return dict_key_to_value(dictionary, entity.get(key, default_value), default_value)
    return None


# 初始化环境信息
def init_envs(env):
    if env == 'PROD':
        receivers = ['jason.lu@wingconn.com', 'sisi.zhong@wingconn.com', 'xiao.liu@wingconn.com','emily.yuan@wingconn.com']
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


# 13位时间戳转格式化日期字符串
def timestamp_to_date_str(time_stamp, format_string="%Y-%m-%d %H:%M:%S"):
    try:
        if time_stamp is None or time_stamp == '':
            return ''
        if len(str(time_stamp)) > 13:
            time_stamp = int(str(time_stamp)[:13])
        elif len(str(time_stamp)) < 13:
            time_stamp = int('{}{}'.format(str(time_stamp), '0' * (10 - len(str(time_stamp)))))

        time_array = time.localtime((time_stamp / 1000))
        return time.strftime(format_string, time_array)
    except BaseException as e:
        print(str(time_stamp))
        return ''


# mysql查询 返回python dict array
def get_mysql_res(sql):
    cursor.execute(sql)
    res = cursor.fetchall()
    return res


# mongo查询 返回python dict array
def get_mongo_res(mongo_client, database, collection, query, projection=None):
    if projection is None:
        results = mongo_client[database][collection].find(query)
    else:
        results = mongo_client[database][collection].find(query, projection)
    return list(results)


def write_data_to_sheet(sheet, sheet_name, titles, data_list):
    sheet.title = sheet_name
    sheet.append(titles)
    if data_list is not None and len(data_list) > 0:
        for row in data_list:
            sheet.append(row)
    for row in sheet.iter_rows():
        for cell in row:
            cell.number_format = '@'


def write_csv_to_zip(path, title, data_list, zip_file):
    with open(path, 'w', encoding='utf-8', newline='') as cf:
        writer = csv.writer(cf)
        writer.writerow(title)
        if data_list is not None:
            for item in data_list:
                for cell in item:
                    if cell is None or cell is 'null':
                        cell = ''
                writer.writerow(item)
    zip_file.write(path)
    os.remove(path)


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


###############################################################################################################
######## 业务相关方法 ###########################################################################################

# 获取目录分类列表
def get_catalogs():
    return get_mongo_res(mongo_client, 'cmp_catalog', 'map_catalog', {},
                         {"_id": 1, "mapCatalogName": 1, "mapCatalogType": 1, "mapCatalogCode": 1,
                          "mapCatalogParentId": 1})


# 获取细目列表
def get_detail_catalogs():
    return get_mongo_res(mongo_client, 'cmp_catalog', 'detail_catalog', {},
                         {"_id": 1, "detailCatalogName": 1, "detailCatalogCode": 1,
                          "catalogParentId": 1})


# 根据目录分类与细目，生成编码转目录分类详情字典，给sheet1使用
def get_info_resource_code_dict():
    # key为编码，value为province、region、catalog、term、catalogue、detail的name
    info_resource_code_dict = {}
    # 目录分类
    catalogs = get_catalogs()
    # 细目
    detail_catalogs = get_detail_catalogs()
    # 获取最上级目录分类
    provinces = [item for item in catalogs if item.get('mapCatalogType', '') == 'province']
    # 目录和细目分类按父id分组
    catalogs.sort(key=lambda d: d['mapCatalogParentId'])
    detail_catalogs.sort(key=lambda d: d['catalogParentId'])
    catalog_dict = {k: list(v) for k, v in itertools.groupby(catalogs, key=lambda d: d['mapCatalogParentId'])}
    detail_catalog_dict = {k: list(v) for k, v in
                           itertools.groupby(detail_catalogs, key=lambda d: d['catalogParentId'])}
    for province_catalog in provinces:
        regions = catalog_dict.get(str(province_catalog['_id']), [])
        if len(regions) == 0:
            info_resource_code = province_catalog.get('mapCatalogCode') + '00000000000000000000'
            info_resource_code_dict[info_resource_code] = {
                'province': province_catalog.get('mapCatalogName', ''),
                'region': None,
                'catalog': None,
                'term': None,
                'catalogue': None,
                'detail': None,
            }
            continue
        for region_catalog in regions:
            categories = catalog_dict.get(str(region_catalog['_id']), [])
            if len(categories) == 0:
                info_resource_code = province_catalog.get('mapCatalogCode') + region_catalog.get(
                    'mapCatalogCode') + '0000000000000000'
                info_resource_code_dict[info_resource_code] = {
                    'province': province_catalog.get('mapCatalogName', ''),
                    'region': region_catalog.get('mapCatalogName', ''),
                    'catalog': None,
                    'term': None,
                    'catalogue': None,
                    'detail': None,
                }
                continue
            for category_catalog in categories:
                terms = catalog_dict.get(str(category_catalog['_id']), [])
                if len(terms) == 0:
                    info_resource_code = province_catalog.get('mapCatalogCode') + region_catalog.get(
                        'mapCatalogCode') + category_catalog.get('mapCatalogCode') + '000000000000000'
                    info_resource_code_dict[info_resource_code] = {
                        'province': province_catalog.get('mapCatalogName', ''),
                        'region': region_catalog.get('mapCatalogName', ''),
                        'catalog': category_catalog.get('mapCatalogName', ''),
                        'term': None,
                        'catalogue': None,
                        'detail': None,
                    }
                    continue
                for term_catalog in terms:
                    catalogues = catalog_dict.get(str(term_catalog['_id']), [])
                    if len(catalogues) == 0:
                        info_resource_code = province_catalog.get('mapCatalogCode') + region_catalog.get(
                            'mapCatalogCode') + category_catalog.get('mapCatalogCode') + term_catalog.get(
                            'mapCatalogCode') + '0000000000000'
                        info_resource_code_dict[info_resource_code] = {
                            'province': province_catalog.get('mapCatalogName', ''),
                            'region': region_catalog.get('mapCatalogName', ''),
                            'catalog': category_catalog.get('mapCatalogName', ''),
                            'term': term_catalog.get('mapCatalogName', ''),
                            'catalogue': None,
                            'detail': None,
                        }
                        continue
                    for catalogue_catalog in catalogues:
                        details = detail_catalog_dict.get(str(catalogue_catalog['_id']), [])
                        if len(details) == 0:
                            info_resource_code = province_catalog.get('mapCatalogCode') + region_catalog.get(
                                'mapCatalogCode') + category_catalog.get('mapCatalogCode') + term_catalog.get(
                                'mapCatalogCode') + catalogue_catalog.get('mapCatalogCode') + '0000000000'
                            info_resource_code_dict[info_resource_code] = {
                                'province': province_catalog.get('mapCatalogName', ''),
                                'region': region_catalog.get('mapCatalogName', ''),
                                'catalog': category_catalog.get('mapCatalogName', ''),
                                'term': term_catalog.get('mapCatalogName', ''),
                                'catalogue': catalogue_catalog.get('mapCatalogName', ''),
                                'detail': None,
                            }
                            continue
                        for detail in details:
                            info_resource_code = province_catalog.get('mapCatalogCode') + region_catalog.get(
                                'mapCatalogCode') + category_catalog.get('mapCatalogCode') + term_catalog.get(
                                'mapCatalogCode') + catalogue_catalog.get('mapCatalogCode') + detail.get(
                                'detailCatalogCode')
                            info_resource_code_dict[info_resource_code] = {
                                'province': province_catalog.get('mapCatalogName', ''),
                                'region': region_catalog.get('mapCatalogName', ''),
                                'catalog': category_catalog.get('mapCatalogName', ''),
                                'term': term_catalog.get('mapCatalogName', ''),
                                'catalogue': catalogue_catalog.get('mapCatalogName', ''),
                                'detail': detail.get('detailCatalogName', ''),
                            }
    # 释放内存
    del catalogs
    del detail_catalogs
    del catalog_dict
    del detail_catalog_dict
    gc.collect()
    return info_resource_code_dict


# 获取目录列表(sheet1不需要省级数据，sheet5需要但不需要那么多字段，分次查询)
# 统计不需要省级数据，但是第五个sheet中申请会涉及到申请省级资源，要目录信息，所以只能全查了
def get_info_resources(regioncode):
    sql = "select id, dept_info_resource_code, base_info_resource_code, theme_info_resource_code, info_resource_life_cycle, report_status, info_resource_name, org_name, org_code,info_resource_provider,info_resource_provider_code, info_resource_located_sys, source_departments_text, info_resource_desc, storage_modes, info_item_desc_detail, update_cycle, remarks, related_task_flag, task_guid, task_name, task_type, basic_catalog_code, business_handling_code, implement_list_code,unrelated_task_reason, nettype, certification_type,gov_use_scene, other_use_scene,field_type,other_field_type,share_type,share_mode,share_condition,not_share_reason_type,is_open,open_type,open_condition, not_open_reason_type, belong_industry, use_scene, resource_subject from cmp_catalog.info_resource_platform where regioncode = '%s' order by regioncode desc"
    return get_mysql_res(sql % regioncode)


def get_province_info_resources_to_info_resource_global_info(info_resource_global_dict):
    sql = "select id, dept_info_resource_code, base_info_resource_code, theme_info_resource_code, info_resource_life_cycle, report_status, info_resource_name, org_name, org_code,info_resource_provider,info_resource_provider_code,source_departments_text from cmp_catalog.info_resource_platform where regioncode = '%s' order by update_date desc"
    for regioncode in province_regions:

        info_resources = get_mysql_res(sql % regioncode)
        for item in info_resources:
            info_resource_code = None
            dept_info_resource_code = item.get('dept_info_resource_code', '')
            base_info_resource_code = item.get('base_info_resource_code', '')
            theme_info_resource_code = item.get('theme_info_resource_code', '')
            if dept_info_resource_code is not None and dept_info_resource_code != '':
                info_resource_code = dept_info_resource_code
            elif base_info_resource_code is not None and base_info_resource_code != '':
                info_resource_code = base_info_resource_code
            else:
                info_resource_code = theme_info_resource_code
            convert_info_resource_global_info(item, info_resource_code, info_resource_global_dict)
        del info_resources
        gc.collect()


# 转换为目录全局字典信息
"""
{
        'info_resource_code': '',
        'info_resource_name': '',
        'info_resource_status': '',
        'info_resource_provider': '',
        'info_resource_provider_code': '',
        'source_departments': ''
    }
"""
def convert_info_resource_global_info(info_resource, info_resource_code, info_resource_global_dict):
    info_resource_provider = info_resource.get('info_resource_provider', '')
    if info_resource_provider is None or info_resource_provider == '':
        info_resource_provider = info_resource.get('org_name', '')
    info_resource_provider_code = info_resource.get('info_resource_provider_code', '')
    if info_resource_provider_code is None or info_resource_provider_code == '':
        info_resource_provider_code = info_resource.get('org_code', '')
    # 处理获得目录编码
    # 处理来源方

    source_departments_text = info_resource.get('source_departments_text', '[]')
    source_departments = None
    if source_departments_text is None or source_departments_text == '' or source_departments_text == '[]':
        source_departments = None
    else:
        try:
            source_departments = "、".join(
                [dept.get('deptName', '') for dept in json.loads(info_resource.get('source_departments_text', '[]'))])
        except:
            print(info_resource['info_resource_name'] + " source departments text json loads error")
    info_resource_global_dict[info_resource['id']] = {
        'info_resource_code': info_resource_code,
        'info_resource_name': info_resource.get('info_resource_name', ''),
        'info_resource_status': dict_key_to_value(
            info_res_life_cycle_dict, info_resource.get('info_resource_life_cycle', ''), ''),
        'info_resource_provider': info_resource_provider,
        'info_resource_provider_code': info_resource_provider_code,
        'source_departments': source_departments
    }


# 获取sheet1所需数据，同时转换为目录全局字典，后续sheet统计需用到
def get_info_resource_sheet_row_data_list(regioncode, info_resource_global_dict, info_resource_code_dict,filter_info_resource_id_arr):
    # sheet1数据
    sheet_data_row_list = []
    # 1.查询目录
    info_resources = get_info_resources(regioncode)
    # 2.遍历目录实体数组，转换为全局字典和第一个sheet中的行
    for item in info_resources:
        # 处理获得目录编码
        info_resource_code = None
        dept_info_resource_code = item.get('dept_info_resource_code', '')
        base_info_resource_code = item.get('base_info_resource_code', '')
        theme_info_resource_code = item.get('theme_info_resource_code', '')
        if dept_info_resource_code is not None and dept_info_resource_code != '':
            info_resource_code = dept_info_resource_code
        elif base_info_resource_code is not None and base_info_resource_code != '':
            info_resource_code = base_info_resource_code
        else:
            info_resource_code = theme_info_resource_code
        # 转换为目录全局字典，后续sheet统计需用到
        convert_info_resource_global_info(item, info_resource_code, info_resource_global_dict)

        # 过滤公安17W目录
        if info_resource_code.split('/')[0] == filter_info_resource_code_prefix:
            filter_info_resource_id_arr.append(item['id'])
            continue

        info_items = []
        tasks = []
        # 转换信息项
        try:
            info_items = json.loads(item.get('info_item_desc_detail', ''))
        except:
            print(item['info_resource_name'] + " info item detail json loads error")

        # 是否关联事务，默认值补全
        if item.get('related_task_flag', None) is None:
            if item.get('unrelated_task_reason', None) is not None:
                item['related_task_flag'] = False
            else:
                item['related_task_flag'] = True
        # 转换事务
        try:
            if len(item.get('task_name', '')) > 0:
                task_guids = item.get('task_guid', '').split("|")
                task_names = item.get('task_name', '').split("|")
                task_types = item.get('task_type', '').split("|")
                basic_catalog_codes = item.get('basic_catalog_code', '').split("|")
                business_handling_codes = item.get('business_handling_code', '').split("|")
                implement_list_codes = item.get('implement_list_code', '').split("|")
                for index, task_name in enumerate(task_names):
                    tasks.append({
                        "task_guid": get_element(task_guids, index, ""),
                        "task_name": task_name,
                        "task_type": get_element(task_types, index, ""),
                        "basic_catalog_code": get_element(basic_catalog_codes, index, ""),
                        "business_handling_code": get_element(business_handling_codes, index, ""),
                        "implement_list_code": get_element(implement_list_codes, index, ""),
                    })

        except:
            print(item['info_resource_name'] + " task loads error")

        # 处理是否部门类、主题类、基础类，以及相关信息
        is_dept_catalog = '否'
        detail_catalog_name = None
        is_base_catalog = '否'
        base_first_catalog_name = None
        base_second_catalog_name = None
        is_theme_catalog = '否'
        theme_first_catalog_name = None
        theme_second_catalog_name = None
        if dept_info_resource_code is not None and dept_info_resource_code != '':
            is_dept_catalog = '是'
            detail_catalog_name = info_resource_code_dict.get(dept_info_resource_code.split('/')[0], {}).get(
                'detail',
                None)
        if base_info_resource_code is not None and base_info_resource_code != '':
            is_base_catalog = '是'
            base_catalog_info = info_resource_code_dict.get(base_info_resource_code.split('/')[0], {})
            base_first_catalog_name = base_catalog_info.get('term', None)
            base_second_catalog_name = base_catalog_info.get('catalogue', None)
        if theme_info_resource_code is not None and theme_info_resource_code != '':
            is_theme_catalog = '是'
            theme_catalog_info = info_resource_code_dict.get(theme_info_resource_code.split('/')[0], {})
            theme_first_catalog_name = theme_catalog_info.get('term', None)
            theme_second_catalog_name = theme_catalog_info.get('catalogue', None)

        # 处理共享、开放字段
        share_condition_unconditional = None
        share_condition_conditional = None
        share_condition_no_share = None
        if item.get('share_type') == "无条件共享":
            share_condition_unconditional = item.get('share_condition', None)
        if item.get('share_type') == "有条件共享":
            share_condition_conditional = item.get('share_condition', None)
        if item.get('share_type') == "不予共享":
            share_condition_no_share = item.get('share_condition', None)

        open_condition_open = None
        open_condition_not_open = None
        if item.get('is_open') == "0":
            open_condition_not_open = item.get('open_condition', None)
        else:
            open_condition_open = item.get('open_condition', None)

        # 转换为table_row_data_list
        # 一个目录实体需要占用行数计算
        row_length = max(len(info_items), len(tasks), 1)
        for entity_index in range(row_length):
            info_item = get_element(info_items, entity_index, {})
            task = get_element(tasks, entity_index, {})
            sheet_data_row_list.append([
                # 资源目录代码 dept_info_resource_code, base_info_resource_code, theme_info_resource_code
                write_cell(entity_index, info_resource_code),
                # 状态 info_resource_life_cycle
                entity_to_cell_convert_by_dict(entity_index, info_res_life_cycle_dict, item,
                                               'info_resource_life_cycle',
                                               ''),
                # 省级上报 report_status
                entity_to_cell_convert_by_dict(entity_index, info_resource_report_status_dict, item, 'report_status'),
                # 部门名称,
                write_cell(entity_index,
                           info_resource_global_dict.get(item['id'], {}).get('info_resource_provider', '')),
                # 统一社会信用代码 org_code
                write_cell(entity_index,
                           info_resource_global_dict.get(item['id'], {}).get('info_resource_provider_code', '')),
                # 信息资源名称 info_resource_name
                entity_to_cell(entity_index, item, 'info_resource_name'),
                # 信息主要所属系统 info_resource_located_sys
                entity_to_cell(entity_index, item, 'info_resource_located_sys'),
                # 来源方 source_departments_text
                write_cell(entity_index,
                           info_resource_global_dict.get(item['id'], {}).get('source_departments', '')),
                # 是否属于部门类 dept_info_resource_code
                write_cell(entity_index, is_dept_catalog),
                # 责任处科室
                write_cell(entity_index, detail_catalog_name),
                # 是否属于主题类 theme_info_resource_code
                write_cell(entity_index, is_theme_catalog),
                # 一级主题
                write_cell(entity_index, theme_first_catalog_name),
                # 二级主题
                write_cell(entity_index, theme_second_catalog_name),
                # 是否属于基础类 base_info_resource_code
                write_cell(entity_index, is_base_catalog),
                # 一级分类
                write_cell(entity_index, base_first_catalog_name),
                # 二级分类
                write_cell(entity_index, base_second_catalog_name),
                # 信息资源目录摘要 info_resource_desc
                entity_to_cell(entity_index, item, 'info_resource_desc'),
                # 资源存储方式 storage_modes
                entity_to_cell_convert_by_dict(entity_index, storage_mode_dict, item, 'storage_modes', ''),
                # 信息项-信息项名称
                info_item.get('infoItemName', None),
                # 信息项-数据类型
                info_item.get('dateType', None),
                # 信息项-数据长度
                info_item.get('length', None),
                # 信息项-数据敏感级别
                dict_key_to_value(sensitive_level_dict, info_item.get('sensitiveLevel', None), None),
                # 信息项-共享类型
                dict_key_to_value(item_share_type_dict, info_item.get('shareType', None), None),
                # 信息项-不共享原因
                info_item.get('notShareReason', None),
                # 信息项-是否开放
                dict_key_to_value(bool_number_string_dict, info_item.get('isOpen', None), None),
                # 更新周期 update_cycle
                entity_to_cell(entity_index, item, 'update_cycle'),
                # 备注信息 remarks
                entity_to_cell(entity_index, item, 'remarks'),
                # 是否关联服务事项 related_task_flag
                entity_to_cell_convert_by_dict(entity_index, bool_dict, item, 'related_task_flag'),
                # 事项类型
                task_type_dict.get(task.get('task_type', None), None),
                # 数据所属事项名称
                task.get('task_name', None),
                # 基本目录编码
                task.get('basic_catalog_code', None),
                # 业务办理项编码
                task.get('business_handling_code', None),
                # 实施清单编码
                task.get('implement_list_code', None),
                # 未关联服务事项原因 unrelated_task_reason
                entity_to_cell(entity_index, item, 'unrelated_task_reason'),
                # 提供渠道 nettype
                entity_to_cell_convert_by_dict(entity_index, net_type_dict, item, 'nettype', None),
                # 是否电子证照 certification_type
                entity_to_cell_convert_by_dict(entity_index, certification_type_dict, item, 'certification_type',
                                               None),
                # 应用场景 gov_use_scene
                entity_to_cell_convert_by_dict(entity_index, gov_use_scene_dict, item, 'gov_use_scene', None),
                # 其他应用场景 other_use_scene
                entity_to_cell(entity_index, item, 'other_use_scene'),
                # 事项目录所属领域 field_type
                entity_to_cell_convert_by_dict(entity_index, field_type_dict, item, 'field_type', None),
                # 其他所属领域 other_field_type
                entity_to_cell(entity_index, item, 'other_field_type'),
                # 共享类型 share_type
                entity_to_cell(entity_index, item, 'share_type'),
                # 共享方式 share_mode
                entity_to_cell(entity_index, item, 'share_mode'),
                # 使用要求 share_condition
                write_cell(entity_index, share_condition_unconditional),
                # 共享条件 share_condition
                write_cell(entity_index, share_condition_conditional),
                # 不予共享原因 not_share_reason_type
                entity_to_cell_convert_by_dict(entity_index, reason_type_dict, item, 'not_share_reason_type', None),
                # 详细说明 share_condition
                write_cell(entity_index, share_condition_no_share),
                # 是否向社会开放 is_open
                entity_to_cell_convert_by_dict(entity_index, bool_number_string_dict, item, 'is_open', None),
                # 开放类型 open_type
                entity_to_cell_convert_by_dict(entity_index, open_type_dict, item, 'open_type', None),
                # 开放条件 open_condition
                write_cell(entity_index, open_condition_open),
                # 不开放依据 not_open_reason_type
                entity_to_cell_convert_by_dict(entity_index, reason_type_dict, item, 'not_open_reason_type', None),
                # 详细说明 open_condition
                write_cell(entity_index, open_condition_not_open),
                # 目录分类（按行业）belong_industry
                entity_to_cell_convert_by_dict(entity_index, belong_industry_dict, item, 'belong_industry', None),
                # 目录分类（按主题）use_scene
                entity_to_cell_convert_by_dict(entity_index, use_scene_dict, item, 'use_scene', None),
                # 所属领域 resource_subject
                entity_to_cell_convert_by_dict(entity_index, resource_subject_dict, item, 'resource_subject', None),
                # id
                write_cell(entity_index, item.get('id')),
            ])

    # 释放内存
    del info_resources
    gc.collect()
    return sheet_data_row_list


def convert_to_data_resource_global(data_resource_global_dict, resource_id, resource_name, info_resource_id,
                                    info_resource_name):
    data_resource_global_dict[resource_id] = {
        'resource_name': resource_name,
        'info_resource_id': info_resource_id,
        'info_resource_name': info_resource_name
    }


# 获取资源上报信息
def get_share_data_resource_report_info():
    sql = "select resource_id, report_status from data_share_db.share_data_resource"
    share_data_resources = get_mysql_res(sql)
    data_res_report_dict = {}
    for item in share_data_resources:
        data_res_report_dict[item['resource_id']] = item.get('report_status', '')
    # 释放内存
    del share_data_resources
    gc.collect()
    return data_res_report_dict


def get_file_resource_sheet_row_data_list(info_resource_global_dict, data_resource_global_dict, data_res_report_dict):
    file_resources = get_mongo_res(mongo_client, 'data_share_db', 'file_data_resource',
                                   {'related_catalog_info.region_code': {'$nin': ['0000', '1111']}},
                                   {'_id': 1, 'info_resource_id': 1, 'info_resource_name': 1, 'status': 1,
                                    'file_name': 1, 'is_struct': 1,
                                    'share_range': 1, 'update_cycle': 1, "share_condition": 1, "file_desc": 1,
                                    "use_range": 1, "inner_audit": 1, "other_files": 1, "info_items": 1})
    sheet_data_row_list = []
    for item in file_resources:
        resource_id = str(item['_id'])
        convert_to_data_resource_global(data_resource_global_dict, resource_id, item.get('file_name'),
                                        item.get('info_resource_id', None), item.get('info_resource_name', None))
        info_res = info_resource_global_dict.get(item.get('info_resource_id', ''), {})
        report_status = dict_key_to_value(report_status_dict, data_res_report_dict.get(resource_id, ''), '未发布')
        attachments = item.get('other_files', [])
        info_items = item.get('info_items', [])
        row_length = max(len(info_items), len(attachments), 1)
        for entity_index in range(row_length):
            attachment = get_element(attachments, entity_index, {})
            info_item = get_element(info_items, entity_index, {})
            sheet_data_row_list.append([
                # 资源目录代码
                entity_to_cell(entity_index, info_res, 'info_resource_code'),
                # 资源目录名称
                entity_to_cell(entity_index, info_res, 'info_resource_name'),
                # 状态
                entity_to_cell_convert_by_dict(entity_index, data_res_status_dict, item, 'status', ''),
                # 省级上报状态
                write_cell(entity_index, report_status),
                # 提供方统一社会信用代码
                entity_to_cell(entity_index, info_res, 'info_resource_provider_code'),
                # 提供方部门名称
                entity_to_cell(entity_index, info_res, 'info_resource_provider'),
                # 文件资源名称
                entity_to_cell(entity_index, item, 'file_name'),
                # 文件资源分类
                entity_to_cell(entity_index, item, 'is_struct'),
                # 共享类型
                entity_to_cell(entity_index, item, 'share_range'),
                # 更新周期
                entity_to_cell_convert_by_dict(entity_index, update_cycle_dict, item, 'update_cycle', ''),
                # 共享需求
                entity_to_cell(entity_index, item, 'share_condition'),
                # 资源描述
                entity_to_cell(entity_index, item, 'file_desc'),
                # 使用范围
                entity_to_cell(entity_index, item, 'use_range'),
                # 需要其他部门审核
                entity_to_cell_convert_by_dict(entity_index, bool_yn_dict, item, 'inner_audit'),
                # 来源方
                entity_to_cell(entity_index, info_res, 'source_departments'),
                # 附件
                attachment.get('name', ''),
                # 附件说明
                attachment.get('file_desc', ''),
                # 字段名称
                info_item.get('item_name', ''),
                # 字段描述
                info_item.get('item_desc', ''),
                # 字段类型
                info_item.get('item_type', ''),
                # 长度
                info_item.get('item_length', ''),
                # TODO:业务信息 自定义表单，暂时不处理
                None,
                write_cell(entity_index, str(item.get('_id'))),
                write_cell(entity_index, item.get('info_resource_id', '')),
            ])
    # 释放内存
    del file_resources
    gc.collect()
    return sheet_data_row_list


def get_province_file_resources_to_data_resource_global_info(data_resource_global_dict):
    file_resources = get_mongo_res(mongo_client, 'data_share_db', 'file_data_resource',
                                   {'related_catalog_info.region_code': {'$in': ['0000', '1111']}},
                                   {'_id': 1, 'info_resource_id': 1, 'info_resource_name': 1, 'file_name': 1})
    for item in file_resources:
        convert_to_data_resource_global(data_resource_global_dict, str(item.get('_id')), item.get('file_name'),
                                        item.get('info_resource_id', None), item.get('info_resource_name', None))
    # 释放内存
    del file_resources
    gc.collect()


def get_api_resource_sheet_row_data_list(info_resource_global_dict, data_resource_global_dict, data_res_report_dict, filter_info_resource_id_arr):
    api_resources = get_mongo_res(mongo_client, 'data_share_db', 'api_data_resource',
                                  {'related_catalog_info.region_code': {'$nin': ['0000', '1111']}},
                                  {'_id': 1, 'info_resource_id': 1, 'info_resource_name': 1, 'status': 1, 'api_name': 1,
                                   'api_url': 1, 'url_map_mode':1,
                                   'apiGatewayEntity': 1, 'api_desc': 1, 'api_protocol': 1, 'api_method': 1,
                                   'share_range': 1, 'update_cycle': 1, "share_condition": 1,
                                   "use_range": 1, "inner_audit": 1, "other_files": 1, "creater_dep_name":1})
    sheet_data_row_list = []
    for item in api_resources:
        resource_id = str(item['_id'])
        convert_to_data_resource_global(data_resource_global_dict, resource_id, item.get('api_name'),
                                        item.get('info_resource_id', None), item.get('info_resource_name', None))
        if item.get('creater_dep_name','') == '苏州市公安局' and item.get('info_resource_id', '') in filter_info_resource_id_arr:
            continue
        report_status = dict_key_to_value(report_status_dict, data_res_report_dict.get(resource_id, ''), '未发布')
        info_res = info_resource_global_dict.get(item.get('info_resource_id', ''), {})
        api_entity = item.get('apiGatewayEntity', {})
        max_rate_sec = api_entity.get('max_rate_sec', '0')
        if max_rate_sec == '' or max_rate_sec is None:
            max_rate_sec = '0'
        max_rate_minute = api_entity.get('max_rate_minute', '0')
        if max_rate_minute == '' or max_rate_minute is None:
            max_rate_minute = '0'
        max_rate_hour = api_entity.get('max_rate_hour', '0')
        if max_rate_hour == '' or max_rate_hour is None:
            max_rate_hour = '0'
        max_rate_day = api_entity.get('max_rate_day', '0')
        if max_rate_day == '' or max_rate_day is None:
            max_rate_day = '0'
        if max_rate_sec == '0' and max_rate_minute == '0' and max_rate_hour == '0' and max_rate_day == '0':
            is_limit = '否'
            max_sec = ''
            frequency = ''
        else:
            is_limit = '是'
            max_sec = max_rate_sec
            if max_rate_day != '0':
                frequency = str(max_rate_day) + "次/天"
            elif max_rate_hour != '0':
                frequency = str(max_rate_hour) + "次/时"
            elif max_rate_minute != '0':
                frequency = str(max_rate_minute) + "次/分"
            else:
                frequency = ''


        attachments = "、".join([attachment.get('name', '') for attachment in item.get('other_files', [])])
        sheet_data_row_list.append([
            # 资源目录代码
            info_res.get('info_resource_code', None),
            # 资源目录名称
            info_res.get('info_resource_name', None),
            # 状态
            dict_key_to_value(data_res_status_dict, item.get('status', ''), ''),
            # 省级上报状态
            report_status,
            # 提供方统一社会信用代码
            info_res.get('info_resource_provider_code', None),
            # 提供方部门名称
            info_res.get('info_resource_provider', None),
            # 接口名称
            item.get('api_name', ''),
            # 接口地址
            item.get('api_url', ''),
            # 匹配模式
            dict_key_to_value(url_map_mode_dict, item.get('url_map_mode', 'absolute')),
            # 接口描述
            item.get('api_desc', ''),
            # 请求方式
            item.get('api_method', ''),
            # 请求类型
            dict_key_to_value(api_protocol_dict, item.get('api_protocol', ''), ''),
            # 共享类型
            item.get('share_range', ''),
            # 更新周期
            dict_key_to_value(update_cycle_dict, item.get('update_cycle', '')),
            # 共享要求
            item.get('share_condition', ''),
            # 是否限流
            is_limit,
            # 每秒最大流量
            max_sec,
            # 可供调用频次
            frequency,
            # 需要其他部门审核
            dict_key_to_value(bool_yn_dict, item.get('inner_audit', ''), ''),
            # 来源方
            info_res.get('source_departments', ''),
            # 附件
            attachments,
            str(item.get('_id')),
            item.get('info_resource_id', ''),
        ])
    # 释放内存
    del api_resources
    gc.collect()
    return sheet_data_row_list


def get_province_api_resources_to_data_resource_global_info(data_resource_global_dict):
    api_resources = get_mongo_res(mongo_client, 'data_share_db', 'api_data_resource',
                                  {'related_catalog_info.region_code': {'$in': ['0000', '1111']}},
                                  {'_id': 1, 'info_resource_id': 1, 'info_resource_name': 1, 'api_name': 1})
    for item in api_resources:
        convert_to_data_resource_global(data_resource_global_dict, str(item.get('_id')), item.get('api_name'),
                                        item.get('info_resource_id', None), item.get('info_resource_name', None))
    # 释放内存
    del api_resources
    gc.collect()


def get_table_resource_sheet_row_data_list(info_resource_global_dict, data_resource_global_dict, data_res_report_dict):
    table_resources = get_mongo_res(mongo_client, 'data_share_db', 'table_data_resource',
                                    {'related_catalog_info.region_code': {'$nin': ['0000', '1111']}},
                                    {'_id': 1, 'info_resource_id': 1, 'info_resource_name': 1, 'status': 1,
                                     'table_name': 1,
                                     'share_range': 1, 'update_cycle': 1, "share_condition": 1, "table_desc": 1,
                                     "use_range": 1, "inner_audit": 1, "other_files": 1, "info_items": 1})
    sheet_data_row_list = []
    for item in table_resources:
        resource_id = str(item['_id'])
        convert_to_data_resource_global(data_resource_global_dict, resource_id, item.get('table_name'),
                                        item.get('info_resource_id', None), item.get('info_resource_name', None))
        report_status = dict_key_to_value(report_status_dict, data_res_report_dict.get(resource_id, ''), '未发布')
        info_res = info_resource_global_dict.get(item.get('info_resource_id', ''), {})
        attachments = "、".join([attachment.get('name', '') for attachment in item.get('other_files', [])])
        info_items = item.get('info_items', [])
        row_length = max(len(info_items), 1)
        for entity_index in range(row_length):
            info_item = get_element(info_items, entity_index, {})
            sheet_data_row_list.append([
                # 资源目录代码
                entity_to_cell(entity_index, info_res, 'info_resource_code'),
                # 资源目录名称
                entity_to_cell(entity_index, info_res, 'info_resource_name'),
                # 状态
                entity_to_cell_convert_by_dict(entity_index, data_res_status_dict, item, 'status', ''),
                # 省级上报状态
                write_cell(entity_index, report_status),
                # 提供方统一社会信用代码
                entity_to_cell(entity_index, info_res, 'info_resource_provider_code'),
                # 提供方部门名称
                entity_to_cell(entity_index, info_res, 'info_resource_provider'),
                # 库表资源名称
                entity_to_cell(entity_index, item, 'table_name'),
                # 共享类型
                entity_to_cell(entity_index, item, 'share_range'),
                # 更新周期
                entity_to_cell_convert_by_dict(entity_index, update_cycle_dict, item, 'update_cycle', ''),
                # 共享需求
                entity_to_cell(entity_index, item, 'share_condition'),
                # 资源描述
                entity_to_cell(entity_index, item, 'table_desc'),
                # 申请范围
                entity_to_cell(entity_index, item, 'use_range'),
                # 需要其他部门审核
                entity_to_cell_convert_by_dict(entity_index, bool_yn_dict, item, 'inner_audit'),
                # 来源方
                entity_to_cell(entity_index, info_res, 'source_departments'),
                # 附件
                attachments,
                # 字段名称
                info_item.get('item_name', ''),
                # 字段描述
                info_item.get('item_desc', ''),
                # 字段长度
                info_item.get('item_length', ''),

                write_cell(entity_index, str(item.get('_id'))),
                write_cell(entity_index, item.get('info_resource_id', '')),
            ])
    # 释放内存
    del table_resources
    gc.collect()
    return sheet_data_row_list


def get_province_table_resources_to_data_resource_global_info(data_resource_global_dict):
    table_resources = get_mongo_res(mongo_client, 'data_share_db', 'table_data_resource',
                                    {'related_catalog_info.region_code': {'$nin': ['0000', '1111']}},
                                    {'_id': 1, 'info_resource_id': 1, 'info_resource_name': 1, 'table_name': 1})
    for item in table_resources:
        convert_to_data_resource_global(data_resource_global_dict, str(item.get('_id')), item.get('table_name'),
                                        item.get('info_resource_id', None), item.get('info_resource_name', None))
    # 释放内存
    del table_resources
    gc.collect()


def get_apply_sheet_row_data_list(info_resource_global_dict, data_resource_global_dict):
    applies = get_mongo_res(mongo_client, 'data_share_db', 'data_resource_apply',
                            {},
                            {'_id': 1, 'resource_id': 1, 'share_resource_id': 1, 'resource_name': 1, 'code': 1,
                             'apply_type': 1, 'dep_name': 1, "dep_code": 1, "apply_time": 1,
                             "status": 1, "admin_audit_time": 1, "admin_audit_time_length": 1,
                             "provider_audit_time": 1, "provider_audit_time_length": 1})
    sheet_data_row_list = []
    for item in applies:
        if item.get('code', None) is None or item.get('code', None) == '':
            continue
        # 根据资源id获取内存缓存的资源信息
        data_res = data_resource_global_dict.get(item.get('resource_id', ''), {})
        # 根据目录id获取内存缓存的目录信息
        info_res = info_resource_global_dict.get(data_res.get('info_resource_id', ''), {})
        sheet_data_row_list.append([
            # 申请流水号
            str(item.get('code', ''))+"\t",
            # 资源名称
            data_res.get('resource_name', item.get('resource_name', None)),
            # 资源类型
            dict_key_to_value(resource_type_dict, item.get('apply_type', ''), ''),
            # 资源目录代码
            info_res.get('info_resource_code', None),
            # 资源目录名称
            info_res.get('info_resource_name', data_res.get('info_resource_name', None)),
            # 提供方统一社会信用代码
            str(info_res.get('info_resource_provider_code', ''))+"\t",
            # 提供方部门名称
            info_res.get('info_resource_provider', None),
            # 申请方统一社会信用代码
            str(item.get('dep_code', ''))+"\t",
            # 申请方部门名称
            item.get('dep_name', None),
            # 发起时间
            timestamp_to_date_str(item.get('apply_time', '')),
            # 状态
            dict_key_to_value(apply_status_dict, item.get('status', ''), item.get('status', '')),
            # 平台管理员受理审批完成时间
            timestamp_to_date_str(item.get('apply_time', '')),
            # 受理审批时长
            item.get('admin_audit_time_length', None),
            # 提供部门授权审批完成时间
            timestamp_to_date_str(item.get('apply_time', '')),
            # 授权审批时长
            item.get('provider_audit_time_length', None),

            str(item.get('_id')),
            item.get('resource_id', ''),
            data_res.get('info_resource_id', '')
        ])
    # 释放内存
    del applies
    gc.collect()
    return sheet_data_row_list


if __name__ == '__main__':
    mongo_client, cursor, receivers = init_envs(env)

    # 目录全局数据字典，多个sheet会使用，key为目录主键，value包含："资源目录代码", "资源目录名称", "状态", "提供方统一社会信用代码"
    info_resource_global_dict = {}
    # 过滤目录id列表(公安17W目录和其资源不导出)
    filter_info_resource_id_arr = []
    zip_file_path = file_context + '.zip'
    if os.path.exists(zip_file_path):
        os.remove(zip_file_path)
    zip_file = zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED)

    # sheet1 信息资源目录表
    # 0.获取目录编码对应目录信息字典 key为编码，value为province、region、catalog、term、catalogue、detail的name
    info_resource_code_dict = get_info_resource_code_dict()
    print('export info resource to table started at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    info_res_sheet_title = ['资源目录代码', '状态', '省级上报', '部门名称', '统一社会信用代码', '信息资源名称',
                            '信息主要所属系统', '来源方', '是否属于部门类', '责任处科室', '是否属于主题类', '一级主题',
                            '二级主题', '是否属于基础类', '一级分类', '二级分类', '信息资源目录摘要', '资源存储方式',
                            '信息项-信息项名称', '信息项-数据类型', '信息项-数据长度', '信息项-数据敏感级别',
                            '信息项-共享类型', '信息项-不共享原因', '信息项-是否开放', '更新周期', '备注信息',
                            '是否关联服务事项', '事项类型', '数据所属事项名称', '基本目录编码', '业务办理项编码',
                            '实施清单编码', '未关联服务事项原因', '提供渠道', '是否电子证照', '应用场景',
                            '其他应用场景', '事项目录所属领域', '其他所属领域', '共享类型', '共享方式', '使用要求',
                            '共享条件', '不予共享原因', '详细说明', '是否向社会开放', '开放类型', '开放条件',
                            '不开放依据', '详细说明', '目录分类（按行业）', '目录分类（按主题）', '所属领域', '目录ID']
    all_sheet_data_row_list = []
    sheet_data_row_list = get_info_resource_sheet_row_data_list(city_region,info_resource_global_dict,info_resource_code_dict,filter_info_resource_id_arr)
    all_sheet_data_row_list.extend(sheet_data_row_list)
    write_csv_to_zip('信息资源目录表-'+dict_key_to_value(region_code_to_name_dict, city_region, city_region)+'.csv', info_res_sheet_title, sheet_data_row_list, zip_file)
    for regioncode in area_regions:
        sheet_data_row_list = get_info_resource_sheet_row_data_list(regioncode, info_resource_global_dict, info_resource_code_dict,filter_info_resource_id_arr)
        all_sheet_data_row_list.extend(sheet_data_row_list)
        write_csv_to_zip('信息资源目录表-'+dict_key_to_value(region_code_to_name_dict, regioncode, regioncode)+'.csv', info_res_sheet_title, sheet_data_row_list, zip_file)
    write_csv_to_zip('信息资源目录表-.csv', info_res_sheet_title, all_sheet_data_row_list, zip_file)
    del info_resource_code_dict
    del sheet_data_row_list
    del all_sheet_data_row_list
    gc.collect()
    # 补上省级目录信息（给后面用）
    get_province_info_resources_to_info_resource_global_info(info_resource_global_dict)
    print('export info resource to csv ended at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    ### sheet1（目录）统计完毕

    data_res_report_dict = get_share_data_resource_report_info()
    # 信息资源全局信息字典, 申请(sheet5)要使用，需包含省级资源
    data_resource_global_dict = {}
    # sheet2 文件资源表
    print('export file resource to csv started at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    file_res_sheet_title = ["资源目录代码", "资源目录名称", "状态", "省级上报状态", "提供方统一社会信用代码",
                            "提供方部门名称", "文件资源名称", "文件资源分类", "共享类型", "更新周期", "共享需求",
                            "资源描述", "使用范围", "需要其他部门审核", "来源方", "附件", "附件说明", "字段名称",
                            "字段描述", "字段类型", "长度", "业务信息", '文件资源ID', '目录ID']
    sheet_data_row_list = get_file_resource_sheet_row_data_list(info_resource_global_dict, data_resource_global_dict,
                                                                data_res_report_dict)
    write_csv_to_zip('文件资源表.csv', file_res_sheet_title, sheet_data_row_list, zip_file)
    del sheet_data_row_list
    gc.collect()
    # 补上省级资源信息（给后面用）
    get_province_file_resources_to_data_resource_global_info(data_resource_global_dict)
    print('export file resource to csv ended at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # # sheet3 接口资源表
    print('export api resource to csv started at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    api_res_sheet_title = ["资源目录代码", "资源目录名称", "状态", "省级上报状态", "提供方统一社会信用代码",
                           "提供方部门名称", "接口名称", "接口地址", "匹配模式", "接口描述", "请求方式", "请求类型",
                           "共享类型", "更新周期", "共享要求", "是否限流", "每秒最大流量", "可供调用频次",
                           "需要其他部门审核", "来源方", "附件", '接口资源ID', '目录ID']
    sheet_data_row_list = get_api_resource_sheet_row_data_list(info_resource_global_dict, data_resource_global_dict,
                                                               data_res_report_dict, filter_info_resource_id_arr)
    write_csv_to_zip('接口资源表.csv', api_res_sheet_title, sheet_data_row_list, zip_file)
    del sheet_data_row_list
    gc.collect()
    # 补上省级资源信息（给后面用）
    get_province_api_resources_to_data_resource_global_info(data_resource_global_dict)
    print('export api resource to csv ended at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # # sheet4 库表资源表
    print('export table resource to csv started at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    table_res_sheet_title = ["资源目录代码", "资源目录名称", "状态", "省级上报状态", "提供方统一社会信用代码",
                             "提供方部门名称", "库表资源名称", "共享类型", "更新周期", "共享需求", "资源描述",
                             "申请范围", "需要其他部门审核", "来源方", "附件", "字段名称", "字段描述", "字段长度",
                             '库表资源ID', '目录ID']
    sheet_data_row_list = get_table_resource_sheet_row_data_list(info_resource_global_dict, data_resource_global_dict,
                                                                 data_res_report_dict)
    write_csv_to_zip('库表资源表.csv', table_res_sheet_title, sheet_data_row_list, zip_file)
    del sheet_data_row_list
    gc.collect()
    # 补上省级资源信息（给后面用）
    get_province_table_resources_to_data_resource_global_info(data_resource_global_dict)
    print('export table resource to csv ended at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # sheet5 资源申请受理及授权时长表
    print('export apply to csv started at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    apply_sheet_title = [
        "申请流水号", "资源名称", "资源类型", "资源目录代码", "资源目录名称", "提供方统一社会信用代码",
        "提供方部门名称", "申请方统一社会信用代码", "申请方部门名称", "发起时间", "状态", "平台管理员受理审批完成时间",
        "受理审批时长", "提供部门授权审批完成时间", "授权审批时长",'申请ID', '库表资源ID', '目录ID'
    ]

    sheet_data_row_list = get_apply_sheet_row_data_list(info_resource_global_dict, data_resource_global_dict)
    write_csv_to_zip('资源申请受理及授权时长表.csv', apply_sheet_title, sheet_data_row_list, zip_file)
    del sheet_data_row_list
    gc.collect()
    print('export apply to csv ended at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    zip_file.close()

    ### 发送邮件
    if env == 'PROD':
        smtp_host = 'mail.xxzx.suzhou.gov.cn'
        sender = 'superdop@xxzx.suzhou.gov.cn'
        passowrd = 'suzhou@12kfpt'
    else:
        smtp_host = 'smtp.163.com'
        sender = 'rikurobot@163.com'
        passowrd = 'BDDHTVARWQRQFPFN'
    send_mail(smtp_host, 25, sender, passowrd, receivers,
              Header(
                  '[' + env + ']-[' + file_context + ']' + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                  'utf-8'), zip_file_path)

    print('export task ended at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
