import json
import os
import shutil
import time

import requests

URL_TEMPLATE = 'http://{host}/data-visualization-mgt/api/dataSource'

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
             + 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 Edg/86.0.622.69'


def read_config():
    root = os.getcwd()
    path = root + '/config.json'
    if not os.path.exists(path):
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def add_api(url, headers, api_name, api_url):
    print('add '+api_name)
    data = {
        "name": api_name,
        "dataSourceType": "API",
        "componentIds": [
            "5ea8dd0c1d7f3f0001ee9cff"
        ],
        "dataSourceConfig": {
            "apiName": api_name,
            "apiUrl": api_url,
            "mapFields": [
                {
                    "fieldName": "categories",
                    "mapFieldName": "response.categories"
                },
                {
                    "fieldName": "seriesData.name",
                    "mapFieldName": "response.seriesData.name"
                },
                {
                    "fieldName": "seriesData.data",
                    "mapFieldName": "response.seriesData.data"
                }
            ],
            "aliasMap": {},
            "isCustomData": False
        }
    }
    r = requests.post(url, json=data, headers=headers)
    if r.status_code is 200:
        print('add api successfully')
    else:
        print('add api failed')
        print(r.text)
    return


if __name__ == '__main__':
    config = read_config()
    host = config.get("host")
    cookie = config.get("cookie")
    api_list = config.get('api_list')
    url = URL_TEMPLATE.format(host=host)
    headers = {'user-agent': user_agent, 'cookie': cookie}
    for api in api_list:
        add_api(url, headers, api.get('api_name'), api.get('api_url'))
