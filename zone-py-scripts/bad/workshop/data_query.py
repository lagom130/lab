from workshop import base

env = 'PROD'

if __name__ == '__main__':
    mongo_client, cursor, receivers, mysql_conn = base.init_envs(env)
    temp_hand_report_results = base.get_mongo_res(mongo_client, "data_share_report_db", 'temp_hand_report_result', {'reportResult':True ,'updateTime':{'$gte':1}})
    for item in temp_hand_report_results:
        file_count = len(base.get_mongo_res(mongo_client, "data_share_db", 'file_data_resource',
                                            {'info_resource_id':str(item['_id'])}))
        table_count = len(base.get_mongo_res(mongo_client, "data_share_db", 'table_data_resource',
                                        {'info_resource_id': str(item['_id'])}))
        if file_count>0 or table_count>0:
            print(str(item['_id']) + ' has file '+str(file_count)+', and table '+str(table_count))

