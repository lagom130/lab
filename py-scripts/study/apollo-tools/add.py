import requests

COOKIE = 'JSESSIONID=0A57F5B34DB0756EED73EC9E639601B9'
APP_ID = '301100005015'
ENV = 'DEV'
CLUSTER = 'default'
NAMESPACE = 'application'

HOST = 'ccm-prod.wingconn.cn'

ADD_ITEM_URL_TEMPLATE = 'http://{host}/apps/{app_id}/envs/{env}/clusters/{cluster}/namespaces/{namespace}/item'

RELEASE_URL_TEMPLATE = 'http://{host}/apps/{app_id}/envs/{env}/clusters/{cluster}/namespaces/{namespace}/releases'

ADD_ITEM_URL = ADD_ITEM_URL_TEMPLATE.format(host=HOST,
                                            app_id=APP_ID,
                                            env=ENV,
                                            cluster=CLUSTER,
                                            namespace=NAMESPACE)
RELEASE_URL = RELEASE_URL_TEMPLATE.format(
    host=HOST,
    app_id=APP_ID, env=ENV,
    cluster=CLUSTER,
    namespace=NAMESPACE)

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
             + 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 Edg/86.0.622.69'
headers = {'user-agent': user_agent, 'cookie': COOKIE}


def add_item(key, value, comment):
    print('add:' + key + '=' + value + ' // ' + comment)
    url = ADD_ITEM_URL
    data = {
        "tableViewOperType": "create",
        "key": key,
        "value": value,
        "comment": comment,
        "addItemBtnDisabled": True
    }
    r = requests.post(url, json=data, headers=headers)
    if r.status_code is 200:
        print('add item successfully')
    else:
        print('add item failed')
        print(r.text)
    return


def release():
    print('release new items')
    url = RELEASE_URL

    r = requests.post(url, headers=headers)
    if r.status_code is 200:
        print('release successfully')
    else:
        print('release failed')
        print(r.text)
    return


if __name__ == '__main__':
    add_item('LOGIN_INCORRECT_PASSWORD_LIMIT_FLAG', 'true', '登录密码错误次数限制开关')
    add_item('LOGIN_INCORRECT_KEY', 'login:incorrect:', '登录密码错误记录Key')
    add_item('LOGIN_INCORRECT_MAX', '3', '登录密码错误最大限制次数')
    add_item('LOGIN_INCORRECT_EXPIRED', '300', '登录密码错误次数记录过期时间，单位秒')
    add_item('LOGIN_BAN_KEY', 'login:ban:', '登录密码错误禁用key')
    add_item('LOGIN_BAN_EXPIRED', '600', '登录密码错误次禁用过期时间，单位秒')
    release()
