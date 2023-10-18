import requests

COOKIE = 'JSESSIONID=02CDDE2A17BB69451044543E6C09DE55'

OWNER_T = 'http://ccm-prod.wingconn.cn/apps/by-owner?owner={owner}'
SIT_URL_T = 'http://ccm-prod.wingconn.cn/apps/{appId}/envs/{env}/clusters/default/namespaces'

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
             + 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 Edg/86.0.622.69'
headers = {'user-agent': user_agent, 'cookie': COOKIE}


def get_items(appId, env):
    r = requests.get(SIT_URL_T.format(appId=appId, env=env), headers=headers)
    namespaces = r.json()
    n_list = []
    for ns in namespaces:
        n = {}
        n['name'] = ns['baseInfo']['namespaceName']
        items = ns['items']
        is_list = []
        for item in items:
            is_list.append({
                'key': item['item']['key'],
                'value': item['item']['value'],
                'comment': item['item'].get('item', ''),
            })
        n['items'] = is_list
        n_list.append(n)
    return n_list


def get_all_projects():
    r = requests.get(OWNER_T.format(owner='datamidd'), headers=headers)
    projects = r.json()
    res_list = []
    for p in projects:
        res = {}
        res['appId'] = p['appId']
        res['name'] = p['name']
        res['ns'] = get_items(p['appId'], 'FAT')
        res_list.append(res)
    return res_list


if __name__ == '__main__':
    result = get_all_projects()
    print(result)
