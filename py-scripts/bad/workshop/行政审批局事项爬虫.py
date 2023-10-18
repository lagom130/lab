import datetime
import json
import time

import pymongo
import requests

mongo_client = pymongo.MongoClient("2.46.2.239", 27017, username='admin', password='123@abcd',
                                           directConnection=True)

token = 'MTY5NDc3OEE3RTZCNkQ0RkU2MzU0OEM='
area_code_dict = {
    '320500': '市本级',
    '320505': '高新区(虎丘区)',
    '320506': '吴中区',
    '320507': '相城区',
    '320508': '姑苏区',
    '320509': '吴江区',
    '320581': '常熟市',
    '320582': '张家港市',
    '320583': '昆山市',
    '320585': '太仓市',
    '320590': '工业园区',
}



def post_json(url, token, json={}):
    time.sleep(1)
    authorization = 'Bearer ' + token
    headers = {'Content-Type': 'application/json',
               'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0',
               'Authorization': authorization}
    r = requests.post(url, headers=headers, json=json)
    return r


def get_task_kind_ou(area_code):
    url = 'http://2.46.2.239:8008/rs/ei49u/szbsdt/rest/szbszn/getTaskKindOU'
    # 浏览器头
    headers = {'content-type': 'application/json',
               'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    request_body = {
        'token': 'Epoint_WebSerivce_**##0601',
        'params': {
            'areacode': area_code,
            'currentpage': '1',
            'pagesize': '100'
        }
    }
    r = post_json(url, token=token, json=request_body)
    # 返回信息
    response_body = json.loads(r.text)
    return response_body


def get_task_list(area_code, page_no, page_size):
    url = 'http://2.46.2.239:8008/rs/g1v5p/szbsdt/rest/szbszn/getTaskList'
    # 浏览器头
    headers = {'content-type': 'application/json',
               'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    request_body = {
        'token': 'Epoint_WebSerivce_**##0601',
        'params': {
            'areacode': area_code,
            'serve_type': '',
            'pagesize': page_size,
            'currentpage': page_no
        },
    }
    r = post_json(url, token=token, json=request_body)
    # 返回信息
    response_body = json.loads(r.text)
    return response_body


if __name__ == '__main__':
    start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for area_code in area_code_dict.keys():
        # step1 爬事项共享服务-部门列表
        response_body = get_task_kind_ou(area_code)
        # step1.2 保存
        oulist = response_body['custom']['oulist']
        print('get_task_ou_list --> areaCode=' + area_code + ', list size=' + str(len(oulist)))
        for ou in oulist:
            mongo_client['data_share_db']['szbszn_task_kind_ou'].insert_one(ou)
        # step2.1 爬事项共享服务-事项列表查询
        page_no = 1
        page_size = 100
        loop_flag = True
        while loop_flag:
            task_response_body = get_task_list(area_code, page_no, page_size)
            count = task_response_body['custom']['count']
            task_list = task_response_body['custom']['tasklist']
            print('get_task_list --> pageSize='+str(page_size)+',pageNo='+str(page_no)+',areaCode=' + area_code + ', list size=' + str(len(task_list)))
            if int(count) < page_size:
                loop_flag = False
            else:
                page_no = page_no + 1
            for task in task_list:
                mongo_client['data_share_db']['szbszn_task'].insert_one(task)
    print('task start at:' + start_time)
    print('task completed at:' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print('end!')
