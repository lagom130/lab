# coding=utf8
import datetime
import decimal
import json
import random
import re
import time

import bs4
import requests

import leek_analysis


def get_stock_history(code='zs_399300'):

    today = datetime.datetime.now()
    offset = datetime.timedelta(days=100)
    start_datetime = today - offset
    start_str = start_datetime.strftime('%Y%m%d')
    end_str = today.strftime('%Y%m%d')
    # 实时信息api url
    url = 'https://q.stock.sohu.com/hisHq?code={}&start={}&end={}'.format(code, start_str, end_str)
    # 浏览器头
    headers = {'content-type': 'application/json',
               'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    r = requests.get(url, headers=headers)
    # 返回信息
    content = r.text
    data = json.loads(content)[0]['hq']
    # ['日期','开盘','收盘','涨跌额','涨跌','最低','最高','成交量(手)','成交金额(万)','换手率']
    histories = []
    for i in range(60):
        histories.append({
            'date': data[i][0],  # 日期
            'npv': decimal.Decimal(data[i][2]),  # 净值(收盘价)
            'gr': decimal.Decimal(data[i][4].strip('%')),  # 涨幅(涨跌)
            'open': data[i][1],  # 开盘
            'close': data[i][2],  # 收盘
            'change': data[i][3],  # 涨跌额
            'chg': data[i][4],  # 涨跌
            'low': data[i][5],  # 最低
            'high': data[i][6],  # 最高
            'vol': data[i][7],  # 成交量(手)
            'amount': data[i][8],  # 成交金额(万)
            'exchange': data[i][9],  # 换手率
        })
    return histories


def get_stock_info(code='sz399300'):
    fund = {
        'code': code
    }
    # 实时信息api url
    url = 'http://hq.sinajs.cn/list=%s' % 'sz399300'
    # 浏览器头
    headers = {'content-type': 'application/json',
               'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    r = requests.get(url, headers=headers)
    # 返回信息
    content = r.text
    # 正则表达式
    pattern = r'^var hq_str_sz399300=\"(.*)\";'
    # 查找结果
    search = re.findall(pattern, content)
    # 遍历结果
    for i in search:
        data_str = i
        data_arr = data_str.split(',')
        fund['name'] = data_arr[0]
        # 净值
        fund['npv'] = decimal.Decimal(data_arr[2])
        # 估算净值
        fund['lnpv'] = decimal.Decimal(data_arr[3])
        # 估算涨幅
        fund['lgr'] = ((fund['lnpv'] - fund['npv']) / fund['npv'] * 100).quantize(
            decimal.Decimal('0.00'), decimal.ROUND_HALF_UP)

        fund['fullname'] = '{}-{}'.format(fund['code'], fund['name'])
        fund['late'] = '净值={}元, 估算净值={}元, 估算涨幅={}%'.format(fund['npv'], fund['lnpv'], fund['lgr'])
    return fund


def get_fund_info(code):
    if leek_analysis.SPIDER_SLEEP != 0:
        time.sleep(random.randint(1, leek_analysis.SPIDER_SLEEP))
    fund = {
        'code': code
    }
    # 基金实时信息api url
    url = 'http://fundgz.1234567.com.cn/js/%s.js' % code
    # 浏览器头
    headers = {'content-type': 'application/json',
               'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    r = requests.get(url, headers=headers)
    # 返回信息
    content = r.text
    # content = """jsonpgz({"fundcode":"501019","name":"国泰国证航天军工指数","jzrq":"2020-08-13","dwjz":"1.2327","gsz":"1.2690","gszzl":"2.95","gztime":"2020-08-14 15:00"});"""

    # 正则表达式
    pattern = r'^jsonpgz\((.*)\)'
    # 查找结果
    search = re.findall(pattern, content)
    # 遍历结果
    for i in search:
        data = json.loads(i)
        # 补全信息
        if data['fundcode'] == fund['code']:
            if leek_analysis.TRADING_FLAG is None:
                if leek_analysis.TODAY == data['gztime'][:10]:
                    leek_analysis.TRADING_FLAG = True
                else:
                    leek_analysis.TRADING_FLAG = False
            # 基金名
            fund['name'] = data['name']
            # 净值
            fund['npv'] = decimal.Decimal(data['dwjz'])
            # 估算净值
            fund['lnpv'] = decimal.Decimal(data['gsz'])
            # 估算涨幅
            fund['lgr'] = decimal.Decimal(data['gszzl'])

            fund['fullname'] = '{}-{}'.format(fund['code'], fund['name'])
            fund['late'] = '净值={}元, 估算净值={}元， 估算涨幅={}%'.format(fund['npv'], fund['lnpv'], fund['lgr'])
    return fund


def get_fund_history(code, start=1, end=60):
    time.sleep(random.randint(1, 5))
    size = 30
    page = int(start/size) + 1
    end_page = int((end-start+1)/size)
    histories = []
    get_info_list_len = 0
    pre_histories_len = 0
    while True:
        if(page > end_page):
            break
        # 基金实时信息api url
        url = 'https://fundf10.eastmoney.com/F10DataApi.aspx?type=lsjz&code={}&page={}&per={}'.format(code, str(page),
                                                                                                      str(size))
        # 浏览器头
        headers = {'content-type': 'application/json',
                   'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
        r = requests.get(url, headers=headers)
        # 返回信息
        content = r.text
        # 正则表达式
        pattern = r'^var apidata={ content:\"(.*)\",records:'
        # 查找结果
        search = re.findall(pattern, content)
        # 遍历结果
        for i in search:
            parsed_resp = bs4.BeautifulSoup(i, "html.parser")
        tr_list = parsed_resp.find_all('tr')
        for index in range(1, len(tr_list)):
            get_info_list_len +=1
            td_list = tr_list[index].find_all('td')
            if len(td_list) <= 2:
                continue
            if td_list[3].get_text() == '':
                gr = '0.00'
            else:
                gr = td_list[3].get_text().strip('%')
            histories.append({
                'date': td_list[0].get_text(),
                'npv': td_list[1].get_text(),
                'gr': gr,
                'close': td_list[1].get_text(),  # 单位净值
                'accnav': td_list[2].get_text(),  # 累计净值
                'chg': td_list[3].get_text(),  # 日增长率
            })
        if get_info_list_len >= (end-start+1) or get_info_list_len == pre_histories_len:
            break
        pre_histories_len = get_info_list_len
        page+=1

    return histories


def eastmoney_lnpv(code):
    # 基金实时信息api url
    url = 'http://fund.eastmoney.com/{}.html'.format(code)
    # 浏览器头
    headers = {'content-type': 'application/json',
               'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    r = requests.get(url, headers=headers)
    parsed_resp = bs4.BeautifulSoup(r.content, "html.parser")
    span = parsed_resp.find('span', id='gz_gsz')
    gsz = span.get_text()
    return gsz


if __name__ == '__main__':
    stock = get_stock_history()
    print(stock)