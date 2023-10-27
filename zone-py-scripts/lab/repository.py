# coding=utf8
import datetime
import json
import os
import time

from funs import spider


def upsert_logs(code, new):
    root = os.getcwd()
    path = root + '/data/log/{}.json'.format(code)
    logs_old = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            logs_old = json.load(f)

    logs = [new]

    for item in logs_old:
        if len(logs) >= 12:
            break
        if item['date'] != new['date']:
            logs.append(item)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(logs, ensure_ascii=False, indent=2))
    return logs

def get_logs(code, today):
    root = os.getcwd()
    path = root + '/data/log/{}.json'.format(code)
    if not os.path.exists(path):
        return []
    else:
        with open(path, 'r', encoding='utf-8') as f:
            original_logs = json.load(f)
        if original_logs[0]['date'] == today:
            original_logs.pop(0)
        logs = []
        for log in original_logs:
            if len(logs)>=10:
                break
            logs.append(log)
    return logs


def get_histories(code):
    root = os.getcwd()
    path = root + '/data/{}.json'.format(code)
    if not os.path.exists(path):
        histories = upsert(code)
    else:
        with open(path, 'r') as f:
            histories = json.load(f)
    return histories


def upsert_all():
    update_history_cfg_path = 'conf/update_history_cfg.json'
    with open(update_history_cfg_path, 'r', encoding='utf-8') as f:
        update_history_cfg = json.load(f)
        update_date = update_history_cfg.get('date', None)
        if update_date is not None and update_date == time.strftime("%Y-%m-%d", time.localtime()):
            print("today histories were updated!")
            return
    with open('conf/config.json', 'r', encoding='utf-8') as f:
        cfg = json.load(f)
        for fund in cfg['funds']:
            upsert(fund['code'])
    with open(update_history_cfg_path, 'w', encoding='utf-8') as f:
        update_history_cfg = {
            'date': time.strftime("%Y-%m-%d", time.localtime())
        }
        f.write(json.dumps(update_history_cfg, ensure_ascii=False, indent=2))



def upsert(code):
    root = os.getcwd()
    path = root + '/data/{}.json'.format(code)
    if os.path.exists(path):
        with open(path, 'r') as f:
            histories_old = json.load(f)
            histories_new = spider.get_fund_history(code, 1, 30)
            histories = []
            for item in histories_new:
                if histories_old[0]['date'] == item['date']:
                    print('[{}] code={} update to endpoint, endpoint={}'.format(
                        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), code, item['date']))
                    break
                histories.append(item)
                print('[{}] code={} insert {} data'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), code,
                                                      item['date']))
            for item in histories_old:
                if len(histories) >=250:
                    break
                histories.append(item)

    else:
        print('[{}] code={} not exist local data, insert all data'.format(
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), code))
        histories = spider.get_fund_history(code, 1, 270)
    with open(path, 'w') as f:
        f.write(json.dumps(histories, ensure_ascii=False, indent=2))
    return histories


# def upsert_trading_flag(today, flag):
#     root = os.getcwd()
#     path = root + '/conf/log/trading.json'
#     trading = False
#     if os.path.exists(path):
#         with open(path, 'r') as f:
#             trading_cfg = json.load(f)
#             if len(trading_cfg) > 0 and trading_cfg[0]['date'] == today
#
#     with open(path, 'w', encoding='utf-8') as f:
#         f.write(json.dumps(logs, ensure_ascii=False, indent=2))
#     return logs
#
# def get_trading_flag(today):
#     root = os.getcwd()
#     path = root + '//conf/log/trading.json'
#     if not os.path.exists(path):
#         return []
#     else:
#         with open(path, 'r', encoding='utf-8') as f:
#             original_logs = json.load(f)
#         if original_logs[0]['date'] == today:
#             original_logs.pop(0)
#         logs = []
#         for log in original_logs:
#             if len(logs)>=5:
#                 break
#             logs.append(log)
#     return logs




if __name__ == '__main__':
    root = os.getcwd()
    path = root + '/test/{}.json'.format('a')
    los = []
    with open(path, 'w') as f:
        f.write(json.dumps(los, ensure_ascii=False, indent=2))