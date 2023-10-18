import os
import datetime
from email.header import Header

from bson import ObjectId
from openpyxl.workbook import Workbook

import base



# env = '326'
env = 'DEV'
# env = 'PROD'
receivers = None
mongo_client = None
cursor = None



if __name__ == '__main__':
    mongo_client, cursor, receivers = base.init_envs(env)
    applies = base.get_mongo_res(mongo_client, 'data_share_db', 'data_resource_apply',
                                 {'status': 'finished', 'apply_type': 'API', 'apply_form_type': 'PROVINCE'})
    for apply in applies:
        resource_id = apply.get('resource_id', '')
        # 申请中存储的部门应用主键列表，不是网关的app_id
        dept_app_id_list = apply.get('dept_app_id_list',[])
        province_app_guid = apply.get('province_app_guid', '')
        province_app_key = apply.get('province_app_key', '')
        province_app_secret = apply.get('province_app_secret', '')
        api_resource = base.get_one_mongo_res(mongo_client, 'data_share_db', 'api_data_resource',
                           {'_id':ObjectId(resource_id)})
        if api_resource is None:
            continue
        # 资源中内嵌的网关实体，不是网关数据库中查询到的网关实体
        api_resource_embedded_api_gateway_entity = api_resource.get('apiGatewayEntity',{})
        # 资源中内嵌的网关实体的api_id
        api_id = api_resource_embedded_api_gateway_entity.get('api_id', '')
        if api_id is None or api_id == '':
            continue
        if len(dept_app_id_list)>0:
            for dept_app_id in dept_app_id_list:
                dept_app = base.get_one_mongo_res(mongo_client, 'data_share_db', 'table_dept_app_data',
                                       {'_id': ObjectId()})
                if dept_app is None:
                    continue
                app_id = dept_app.get('app_id', '')
                if app_id is None or app_id == '':
                    continue
                gw_next_level_gateway_app_results = base.get_mongo_res(mongo_client, 'dgp_api_gateway_mgt_dsp',
                                                                       'gw_next_level_gateway_app',
                                                                       {'clientId': province_app_key})
                if len(gw_next_level_gateway_app_results) == 0:
                    base.mongo_insert_one(mongo_client, 'dgp_api_gateway_mgt_dsp', 'gw_next_level_gateway_app',
                                          {
                                              "clientId": province_app_key,
                                              "clientSecret": province_app_secret,
                                              "createDT": datetime.datetime.now(),
                                              "nlgDesc": province_app_guid,
                                              "nlgName": province_app_guid,
                                              "updateDT": datetime.datetime.now()
                                          })

                    gw_next_level_gateway_relation_results = base.get_mongo_res(mongo_client, 'dgp_api_gateway_mgt_dsp',
                                                                                'gw_next_level_gateway_relation',
                                                                                {'apiId': api_id, 'appId': app_id})
                    if len(gw_next_level_gateway_relation_results) == 0:
                        base.mongo_insert_one(mongo_client, 'dgp_api_gateway_mgt_dsp', 'gw_next_level_gateway_relation',
                                              {
                                                  "apiId": api_id,
                                                  "appId": app_id,
                                                  "createDT": datetime.datetime.now(),
                                                  "nlgClientId": province_app_key,
                                                  "updateDT": datetime.datetime.now()
                                              })


    print("end!")