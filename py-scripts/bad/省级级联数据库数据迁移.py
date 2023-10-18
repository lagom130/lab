import datetime
import re

import pymongo

env = '326'
# env = 'PROD'
client = None
db = None

# 集合名称
collection_names = [
    "catalog_report",
    "info_resource_report",
    "api_resource_report",
    "table_resource_report",
    "file_resource_report",
    "apply_subscribe_report",
    "org_region_report",
    "client_app_report",
    "resource_relation",
    "info_resource_relation",
    "apply_relation",
    "category_relation",
    "file_accessory_relation",
    "apply_report",
    "apply_audit_report",
    "down_time",
]

# 手动+gpt-4&calude2整理的所有属性字典
field_dict = {
    'appguid': 'app_guid',
    'appid': 'app_id',
    'appkey': 'app_key',
    'appsecret': 'app_secret',
    'applybasiscontent': 'apply_basis_content',
    'applybasistype': 'apply_basis_type',
    'applyfiles': 'apply_files',
    'applyid': 'apply_id',
    'applytype': 'apply_type',
    'applyuser': 'apply_user',
    'approvalresults': 'approval_results',
    'attach': 'attach',
    'belongappsys': 'belong_app_sys',
    'belongindustry': 'belong_industry',
    'body': 'body',
    'business': 'business',
    'businesstype': 'business_type',
    'callexample': 'call_example',
    'cancelreason': 'cancel_reason',
    'cascadecode': 'cascade_code',
    'cascadeguid': 'cascade_guid',
    'cataid': 'cata_id',
    'catalogbasicinfoid': 'catalog_basic_info_id',
    'catalogcategoryid': 'catalog_category_id',
    'catalogid': 'catalog_id',
    'catalogtitle': 'catalog_title',
    'certificationtype': 'certification_type',
    'cnname': 'cn_name',
    'columnid': 'column_id',
    'columnlist': 'column_list',
    'connectionname': 'connection_name',
    'contact': 'contact',
    'contenttype': 'content_type',
    'count': 'count',
    'createstatus': 'create_status',
    'createtime': 'create_time',
    'creditcode': 'credit_code',
    'dataformat': 'data_format',
    'dbname': 'db_name',
    'defaultcataloguemapcatalogid': 'default_catalogue_map_catalog_id',
    'deptname': 'dept_name',
    'deptno': 'dept_no',
    'desc': 'desc',
    'description': 'description',
    'downloadurl': 'download_url',
    'enname': 'en_name',
    'enddate': 'end_date',
    'fieldid': 'field_id',
    'fieldlink': 'field_link',
    'fieldname': 'field_name',
    'fieldtype': 'field_type',
    'fileid': 'file_id',
    'filename': 'file_name',
    'filestructuremessage': 'file_structure_message',
    'govusescene': 'gov_use_scene',
    'groupcode': 'group_code',
    'groupid': 'group_id',
    'grouplevel': 'group_level',
    'groupname': 'group_name',
    'hassubscribe': 'has_subscribe',
    'inforesourceid': 'info_resource_id',
    'inputparams': 'input_params',
    'internalorgan': 'internal_organ',
    'isauth': 'is_auth',
    'isauthorization': 'is_authorization',
    'isbasic': 'is_basic',
    'isnull': 'is_null',
    'ispk': 'is_pk',
    'itemcode': 'item_code',
    'itemname': 'item_name',
    'length': 'length',
    'managemail': 'manage_mail',
    'mapcatalogid': 'map_catalog_id',
    'mapcatalogtype': 'map_catalog_type',
    'maptogroupcode': 'map_to_group_code',
    'maptogroupid': 'map_to_group_id',
    'methodtype': 'method_type',
    'mustfill': 'must_fill',
    'name': 'name',
    'namecn': 'name_cn',
    'networktype': 'netWork_type',
    'nettype': 'net_type',
    'notsharereason': 'not_share_reason',
    'opencondition': 'open_condition',
    'openconditiondesc': 'open_condition_desc',
    'opentype': 'open_type',
    'opinion': 'opinion',
    'orderid': 'order_id',
    'ordernum': 'order_num',
    'orgcode': 'org_code',
    'orgname': 'org_name',
    'otherfieldtype': 'other_field_type',
    'otherupdatecycle': 'other_update_cycle',
    'otherusescene': 'other_use_scene',
    'output': 'output',
    'outputparams': 'output_params',
    'paramname': 'param_name',
    'paramtype': 'param_type',
    'parentid': 'parent_id',
    'pass': 'pass',
    'path': 'path',
    'phone': 'phone',
    'platformfileid': 'platform_file_id',
    'precision': 'precision',
    'provapplystatus': 'prov_apply_status',
    'provideip': 'provide_ip',
    'provideurl': 'provide_url',
    'provinceapplyid': 'province_apply_id',
    'provincefileid': 'province_file_id',
    'provinceinfo': 'province_info',
    'provinceresourceid': 'province_resource_id',
    'publishedtime': 'published_time',
    'reason': 'reason',
    'receivepath': 'receive_path',
    'refapiid': 'ref_api_id',
    'refapplycode': 'ref_apply_code',
    'refapplyid': 'ref_apply_id',
    'refcatalogid': 'ref_catalog_id',
    'reffileid': 'ref_file_id',
    'refinfoid': 'ref_info_id',
    'refresourceid': 'ref_resource_id',
    'refresourcename': 'ref_resource_name',
    'reftableid': 'ref_table_id',
    'regioncode': 'region_code',
    'regionname': 'region_name',
    'relationtype': 'relation_type',
    'releasetime': 'release_time',
    'remark': 'remark',
    'resplatform': 'res_platform',
    'resregistered': 'res_registered',
    'resusescenes': 'res_use_scenes',
    'resourceformat': 'resource_format',
    'resourceid': 'resource_id',
    'resourcename': 'resource_name',
    'resourcesubject': 'resource_subject',
    'resourcesystemid': 'resource_system_id',
    'resourcetype': 'resource_type',
    'resourceusedeptname': 'resource_use_dept_name',
    'resourcesshortname': 'resources_short_name',
    'sensitivelevel': 'sensitive_level',
    'servicedesc': 'service_desc',
    'servicesharetype': 'service_share_type',
    'sharetype': 'share_type',
    'sharedcondition': 'shared_condition',
    'sharedtype': 'shared_type',
    'sharedway': 'shared_way',
    'startdate': 'start_date',
    'status': 'status',
    'statusupdatetime': 'status_update_time',
    'subscribename': 'subscribe_name',
    'supportform': 'support_form',
    'supporter': 'supporter',
    'supporterphone': 'supporter_phone',
    'tablecolumns': 'table_columns',
    'tablejson': 'table_json',
    'tablename': 'table_name',
    'tablesqlname': 'table_sql_name',
    'tablestructuremessage': 'table_structure_message',
    'targetdatasourceid': 'target_data_source_id',
    'taskguid': 'task_guid',
    'techusename': 'tech_use_name',
    'techusetel': 'tech_use_tel',
    'type': 'type',
    'updatecycle': 'update_cycle',
    'updatefrequency': 'update_frequency',
    'updatetime': 'update_time',
    'url': 'url',
    'useapp': 'use_app',
    'usedemand': 'use_demand',
    'usedesc': 'use_desc',
    'usescene': 'use_scene',
    'usescope': 'use_scope',
    'visitip': 'visit_ip'
}

def init_envs(env):
    if env == 'PROD':
        client = pymongo.MongoClient("2.46.2.239", 27017, username='admin', password='123@abcd',
                                           directConnection=True)
    elif env == '326':
        client = pymongo.MongoClient("10.10.32.6", port=27017)
        client.admin.authenticate('admin', '123@abcd', mechanism='SCRAM-SHA-1')
    else:
        client = pymongo.MongoClient(host="mongo-0.mongo,mongo-1.mongo,mongo-2.mongo`", port=27017)
        client.admin.authenticate('admin', '123@abcd', mechanism='SCRAM-SHA-1')
    return client, client['data_share_report_db']



# mongo查询 返回python dict array
def get_mongo_res(database, collection, query, projection=None):
    if projection is None:
        results = mongo_client[database][collection].f(query)
    else:
        results = mongo_client[database][collection].find(query, projection)
    return list(results)

# 重命名collection，返回旧集合，新集合
def prepare_rename(collection_name):
    db[collection_name].rename('old_'+collection_name)
    return db['old_'+collection_name], db[collection_name]


def rename(name):
    key =name.lower().replace('_', '')
    name = field_dict.get(key, name)
    return name

def process_document(document):
    """递归处理文档中的所有属性"""
    new_document = {}
    for key, value in document.items():
        new_key = rename(key)
        if isinstance(value, dict):
            # 如果值是一个字典，递归处理
            new_value = process_document(value)
        elif isinstance(value, list):
            # 如果值是一个列表，遍历列表中的每个元素
            new_value = []
            for item in value:
                if isinstance(item, dict):
                    # 如果元素是一个字典，递归处理
                    new_item = process_document(item)
                else:
                    new_item = item
                new_value.append(new_item)
        else:
            new_value = value
        new_document[new_key] = new_value
    return new_document


if __name__ == '__main__':
    start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("start at "+str(start_time))
    mongo_client, db = init_envs(env)
    for collection_name in collection_names:
        print("handle collection:"+ collection_name)
        # 重命名旧集合，将数据处理后插入新集合
        source_collection, target_collection = prepare_rename(collection_name)
        # 遍历集合中的所有文档
        cursor = source_collection.find()
        for document in cursor:
            # 递归处理文档中的所有属性
            new_document = process_document(document)
            # 插入新文档
            target_collection.insert_one(new_document)

    end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("start at " + str(start_time) + ", end at "+ str(end_time))
