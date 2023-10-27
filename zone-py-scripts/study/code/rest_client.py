import base64
import datetime
import json
import threading
import gevent
from multiprocessing import Process
from concurrent.futures import ThreadPoolExecutor

import requests

apis = {
    'L01': 'http://apigw.ztfw.sit.wingconn.com/rs/0o2nc/l01',
    'L02': 'http://apigw.ztfw.sit.wingconn.com/rs/g4a1c/l02',
    'L03': 'http://apigw.ztfw.sit.wingconn.com/rs/2x5bd/l03',
    'L04': 'http://apigw.ztfw.sit.wingconn.com/rs/0ceb3/l04',
    'L05': 'http://apigw.ztfw.sit.wingconn.com/rs/1dgm1/05',
    'L06': 'http://apigw.ztfw.sit.wingconn.com/rs/1gjz1/06',
    'L07': 'http://apigw.ztfw.sit.wingconn.com/rs/h8pf5/07',
    'L08': 'http://apigw.ztfw.sit.wingconn.com/rs/05bvi/l08',
    'L09': 'http://apigw.ztfw.sit.wingconn.com/rs/35wza/l09',
    'L10': 'http://apigw.ztfw.sit.wingconn.com/rs/c0c3r/l10',
    'L11': 'http://apigw.ztfw.sit.wingconn.com/rs/yh19h/l11',
    'L12': 'http://apigw.ztfw.sit.wingconn.com/rs/ypn74/l12',
}

clients = {'CG01': {'client_id': 'y5fsgIyT7PID9zM', 'client_secret': 'yUiCAgvf6SURlMV',
                    'token': 'NzdFNENCMzlFN0IwNDk2Mzk0QzU4NUQ=', 'tokenExpireTime': 1671198372076},
           'CG02': {'client_id': 'rGPqHyNNcU2NYlU', 'client_secret': 'cqAzQZBWLwDyPR6',
                    'token': 'M0EyNDYyQTg4MjE5MUZEQUMxOTU1NTg=', 'tokenExpireTime': 1671205966201},
           'CG03': {'client_id': 'faseVJHDYQWHwZ4', 'client_secret': '4nbZ5SM7ByfPQ3Y',
                  'token': 'NzQ0NEM3RjlDNzQ3NDM1RjZBNEU0MDE=', 'tokenExpireTime': 1671205966226},
           'CG04': {'client_id': '0MgBAm5d4XLMsgb', 'client_secret': 'bM16SdTkObKW6T9',
                  'token': 'RUI4NDg5ODlBOTNEMzk4ODJDODBFMjA=', 'tokenExpireTime': 1671205966285},
           'CG05': {'client_id': 'CYOnrev8v9PerME', 'client_secret': '3AshQbQ65HduQqS',
                  'token': 'MkY1NEJEODk1NDU2MTJDMUNBNkJBNEY=', 'tokenExpireTime': 1671205966306},
           'CG06': {'client_id': 'NhJPC58MUpu02X5', 'client_secret': 'v4scmx3o1Cg2247',
                  'token': 'RjlCNDM0MUJCMTIxQzA3RkQ1Q0U4NEQ=', 'tokenExpireTime': 1671205966324},
           'CG07': {'client_id': 'bpAXBfMbtJkSjWo', 'client_secret': 'XtUQtBesIUOMuH5',
                  'token': 'QjUxNEI0NjlEMDBBQkI2Mjk3QjQwMjI=', 'tokenExpireTime': 1671205966350},
           'CG08': {'client_id': 'drflexuhd30XxS9', 'client_secret': 'uvOEU8SpcATDMnN',
                  'token': 'RDIxNDFBMEFEOURDRUQzQjNFREU0QzI=', 'tokenExpireTime': 1671205966371},
           'CG09': {'client_id': 'ytgDsPF8ujbrnXI', 'client_secret': 'nK1JpYCHWCdLYzQ',
                  'token': 'MTQyNDQyQTlDNjA0MkY2MEFFNzY4QTk=', 'tokenExpireTime': 1671205966389},
           'CG10': {'client_id': 'kVJgnsWZzI4I7Iw', 'client_secret': 'FawlzFwK0sPR1nD',
                  'token': 'RTc0NDA1OUI4MkIwNEFCQUY4Qjk0ODA=', 'tokenExpireTime': 1671205966407},
           'CG11': {'client_id': '1p3ryuzMTJpJgw7', 'client_secret': 'SBUtO9QfRV46Io9',
                  'token': 'NjgxNEY4QTg2NjkwN0FGREYyOUI2MjY=', 'tokenExpireTime': 1671205966424}}

threads = []

def get_token_get_auth(client_id, client_secret):
    return 'Basic ' + base64.b64encode((client_id + ':' + client_secret).encode('utf-8')).decode('utf-8')


def get_token_response(authorization):
    url = 'http://authcenter-service:8580/authorizationService/token'
    # 浏览器头
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'Authorization': authorization}
    data = {
        'grantType': 'client_credentials'
    }
    r = requests.post(url, data, headers=headers)
    # 返回信息
    content = r.text
    return json.loads(r.text)['response']


def get_req(url, token, c=None, s=None):
    authorization = 'Bearer ' + token
    params = {
        'c': str(c),
        's': str(s)
    }
    headers = {'Content-Type': 'application/json',
               'Authorization': authorization}
    r = requests.get(url, headers=headers, params=params)
    print(r.content)


def req_unit(ak, ck, c=None, s=None):
    url = apis[ak]
    client = clients[ck]
    token = client['token']
    get_req(url, token, c, s)


def req_units(name_prefix, time, ak, ck, c=None, s=None):
    loop = 0
    while loop < time:
        ix = 0
        while ix <10:
            code = '200'
            sec = 0
            if c is None and ix % 3 == 1:
                if ix % 2 == 1:
                    code = '500'
                else:
                    code = '400'
            if s is None and ix % 3 == 2 and ix % 2 == 1:
                sec = 1
            url = apis[ak]
            client = clients[ck]
            token = client['token']
            thread_name = name_prefix +'-' + code + '-' + str(ix)
            threads.append(threading.Thread(name=thread_name,
                                      target=get_req(url, token, code, int(sec % 2)), daemon=False))
            ix = ix+1
        loop = loop+1

def req_thread_unit(name_prefix, times, ak, ck, c=None, s= None):
    unit_main_thread_name = name_prefix+'-'+ck+'-' + ak + '-' + str(times)
    req_units(unit_main_thread_name, times, ak, ck, c, s)


def arrange(thread_name_prefix):
    req_thread_unit(thread_name_prefix, 11, 'L01', 'CG01')
    req_thread_unit(thread_name_prefix, 10, 'L01', 'CG03', c='200', s=0)
    req_thread_unit(thread_name_prefix, 9, 'L01', 'CG05', c='200', s=0)
    req_thread_unit(thread_name_prefix, 8, 'L01', 'CG07', c='200', s=0)
    req_thread_unit(thread_name_prefix, 7, 'L01', 'CG02', c='200', s=0)
    req_thread_unit(thread_name_prefix, 6, 'L01', 'CG04', c='200', s=0)
    req_thread_unit(thread_name_prefix, 5, 'L01', 'CG06', c='200', s=0)
    req_thread_unit(thread_name_prefix, 4, 'L01', 'CG08', c='200', s=0)
    req_thread_unit(thread_name_prefix, 3, 'L01', 'CG11', c='200', s=0)
    req_thread_unit(thread_name_prefix, 2, 'L01', 'CG10', c='200', s=0)
    req_thread_unit(thread_name_prefix, 1, 'L01', 'CG09', c='200', s=0)
    req_thread_unit(thread_name_prefix, 10, 'L03', 'CG01', c='200', s=0)
    req_thread_unit(thread_name_prefix, 9, 'L05', 'CG01', c='200', s=0)
    req_thread_unit(thread_name_prefix, 8, 'L07', 'CG01', c='200', s=0)
    req_thread_unit(thread_name_prefix, 7, 'L09', 'CG01', c='200', s=0)
    req_thread_unit(thread_name_prefix, 6, 'L02', 'CG01', c='200', s=0)
    req_thread_unit(thread_name_prefix, 5, 'L04', 'CG01', c='200', s=0)
    req_thread_unit(thread_name_prefix, 4, 'L06', 'CG01', c='200', s=0)
    req_thread_unit(thread_name_prefix, 3, 'L08', 'CG01', c='200', s=0)
    req_thread_unit(thread_name_prefix, 2, 'L10', 'CG01', c='200', s=0)
    req_thread_unit(thread_name_prefix, 1, 'L11', 'CG01', c='200', s=0)

if __name__ == '__main__':
    for ck in clients.keys():
        client = clients[ck]
        resp = get_token_response(get_token_get_auth(client['client_id'], client['client_secret']))
        client['token'] = resp['accessToken']
        client['tokenExpireTime'] = resp['tokenExpireTime']
        clients[ck] = client
    loop = 0
    loop_max = 100000
    while(loop < loop_max):
        thread_name_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str('-') + str(loop)
        arrange(thread_name_prefix)
        print('loop='+str(loop))
        loop = loop+1
    print('start threads')
    for t in threads:
        t.start()
    print('over')