import os

import requests

COOKIE = ''

def login():
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
                 + 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 Edg/86.0.622.69'
    headers = {'user-agent': user_agent, 'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'username': 'datamidd',
        'password': '123@abcd'
    }
    r = requests.post(url='http://ccm-prod.wingconn.cn/signin', data=data, headers=headers)
    cookies = r.cookies.get_dict()
    print(cookies)




def getAppConfig():
    print(cookie)
    # url_template = 'http://ccm-prod.wingconn.cn/apps/{app_id}/envs/{env}/clusters/{cluster}/namespaces'
    # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
    #              + 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 Edg/86.0.622.69'
    # headers = {'user-agent': user_agent, 'cookie': cookie}
    # requests.get(url_template.format())


if __name__ == '__main__':
    cookie = '123'
    login()