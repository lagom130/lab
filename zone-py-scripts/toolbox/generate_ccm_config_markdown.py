import requests
import codecs
import os

host = ''
cookie = 'JSESSIONID=6D1DB1F6AC84C5AA5A31B678A610392A'

file_path = 'ccm配置说明.md'

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
        'app_id': '100008003',
        'env': 'DEV',
        'cluster': 'default',
        'namespace': 'application'
    }, {
        'name': 'DMS数据网关',
        'path': '/Common-DataMgtSystem/DataGatewayService',
        'app_id': '100008001',
        'env': 'DEV',
        'cluster': 'default',
        'namespace': 'application'
    }, {
        'name': 'DMS文件网关',
        'path': '/Common-DataMgtSystem/FileGatewayService',
        'app_id': '100008006',
        'env': 'DEV',
        'cluster': 'default',
        'namespace': 'application'
    }, {
        'name': 'DMS AP适配器',
        'path': '/Common-DataMgtSystem/DataApAdapterService',
        'app_id': '100008002',
        'env': 'DEV',
        'cluster': 'default',
        'namespace': 'application'
    }, {
        'name': 'DMS TP 适配器',
        'path': '/Common-DataMgtSystem/DataTpAdapterService',
        'app_id': '100008005',
        'env': 'DEV',
        'cluster': 'default',
        'namespace': 'application'
    }
]

URL = 'http://{host}/apps/{app_id}/envs/{env}/clusters/{cluster}/namespaces/{namespace}'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
             + 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 Edg/86.0.622.69'
headers = {'user-agent': user_agent, 'cookie': cookie}


def parse(fp, name, path, app_id, env, cluster, namespace):
    url = URL.format(host= host, app_id=app_id, env=env, cluster=cluster, namespace=namespace)
    data = requests.get(url, headers=headers).json()
    base_info = data['baseInfo']
    fp.write("{}\n".format('    ## ' + name))
    fp.write("{}\n".format('    ### 节点路径: ' + path))
    fp.write("{}\n".format('    #### AppId: ' + base_info['appId']))
    fp.write("{}\n".format('    #### namespace: ' + base_info['namespaceName']))
    items = data['items']
    fp.write("{}\n".format('    属性名 | 说明 | 示例'))
    fp.write("{}\n".format('    ---|---|---'))
    for items_each in items:
        item = items_each['item']
        key = item['key']
        value = item['value'].replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ')
        comment = ''
        if 'comment' in item:
            comment = item['comment']

        fp.write("{}\n".format('    ' + str(key) + ' | ' + str(comment) + ' | ' + str(value) + ' '))
    fp.write('\n')
    return


if __name__ == '__main__':
    # deleted file when the file is existed
    if os.path.exists(file_path):
        os.remove(file_path)
    with codecs.open(file_path, 'wb', encoding='utf-8') as fp:
        fp.write("{}\n".format('- # 前端'))
        if len(front_service_list) > 0:
            for service in front_service_list:
                parse(fp, service['name'], service['path'], service['app_id'], service['env'],
                      service['cluster'], service['namespace'])
        else:
            fp.write("{}\n".format('    无 '))
        fp.write("{}\n".format('- # 后端'))
        if len(back_service_list) > 0:
            for service in back_service_list:
                parse(fp, service['name'], service['path'], service['app_id'], service['env'],
                      service['cluster'], service['namespace'])
        else:
            fp.write("{}\n".format('    无 '))
    print('file write complete')