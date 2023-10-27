# coding=utf8
import datetime
import json

import requests

today = datetime.datetime.now()
offset = datetime.timedelta(days=100)

start_datetime = today - offset
start_str = start_datetime.strftime('%Y%m%d')
end_str = today.strftime('%Y%m%d')
# 实时信息api url
url = 'https://q.stock.sohu.com/hisHq?code={}&start={}&end={}'.format('zs_399300', start_str, end_str)
# 浏览器头
headers = {
    'content-type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
}
r = requests.get(url, headers=headers)
# 返回信息
content = r.text
data = json.loads(content)[0]['hq']
for i in range(60):
    item = data[i]
    print(item)