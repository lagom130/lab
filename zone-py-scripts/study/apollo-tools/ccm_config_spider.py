import requests

cookie = 'JSESSIONID=DC4B4CD851F4444C28C2AE23BC49259E'

front_service_list = [

    {
        'name': 'bop运营平台',
        'path': '/Comm_BizOperationPortal_biz-operation-mgt',
        'app_id': '100101001',
        'env': 'DEV',
        'cluster': 'default',
        'namespace': 'dms'
    }
]
back_service_list = [

    {
        'name': 'DMS 管理端服务',
        'path': '/Common-DataMgtSystem/DataMgtService',
        'app_id': '500100008003',
        'env': 'DEV',
        'cluster': 'default',
        'namespace': 'application'
    }, {
        'name': 'DMS数据网关',
        'path': '/Common-DataMgtSystem/DataGatewayService',
        'app_id': '500100008001',
        'env': 'DEV',
        'cluster': 'default',
        'namespace': 'application'
    }, {
        'name': 'DMS文件网关',
        'path': '/Common-DataMgtSystem/FileGatewayService',
        'app_id': '500100008006',
        'env': 'DEV',
        'cluster': 'default',
        'namespace': 'application'
    }, {
        'name': 'DMS AP适配器',
        'path': '/Common-DataMgtSystem/DataApAdapterService',
        'app_id': '500100008002',
        'env': 'DEV',
        'cluster': 'default',
        'namespace': 'application'
    }, {
        'name': 'DMS TP 适配器',
        'path': '/Common-DataMgtSystem/DataTpAdapterService',
        'app_id': '500100008005',
        'env': 'DEV',
        'cluster': 'default',
        'namespace': 'application'
    }
]
# URL = 'http://ccm-prod.wingconn.cn/apps/100101001/envs/DEV/clusters/default/namespaces/dms'
URL = 'http://ccm-prod.wingconn.cn/apps/{app_id}/envs/{env}/clusters/{cluster}/namespaces/{namespace}'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
             + 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 Edg/86.0.622.69'
headers = {'user-agent': user_agent, 'cookie': cookie}


def parse(name, path, app_id, env, cluster, namespace):
    url = URL.format(app_id=app_id, env=env, cluster=cluster, namespace=namespace)
    r = requests.get(url, headers=headers)
    data = r.json()
    base_info = data['baseInfo']
    print('    ## ' + name)
    print('    ### 节点路径: ' + path)
    print('    #### AppId: ' + base_info['appId'])
    print('    #### namespace: ' + base_info['namespaceName'])
    items = data['items']
    print('    属性名 | 说明 | 示例')
    print('    ---|---|---')
    for items_each in items:
        item = items_each['item']
        key = item['key']
        value = item['value'].replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ')
        comment = ''
        if 'comment' in item:
            comment = item['comment']

        print('    ' + str(key) + ' | ' + str(comment) + ' | ' + str(value) + ' ')
    print()
    return


if __name__ == '__main__':
    print()
    print()
    print('- # 前端')
    for service in front_service_list:
        parse(service['name'], service['path'], service['app_id'], service['env'],
              service['cluster'], service['namespace'])
    print()
    print('- # 后端')
    for service in back_service_list:
        parse(service['name'], service['path'], service['app_id'], service['env'],
              service['cluster'], service['namespace'])
