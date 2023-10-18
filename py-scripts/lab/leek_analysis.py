# coding=utf8
import datetime
import decimal
import json
import logging
import random
import time

import repository
from funs import spider, analysis

opt_result_format = '【{}】操作建议:{}'

SPIDER_SLEEP = 3

BASIC_STEP = 40
BASIC_DAC_STEP = 40
BASIC_BUILD_STEP = 40
BASIC_BUILD_BIG_STEP = 40
BASIC_GR = 2
BAD_STOP_LONG_BIAS = 0.08
GOOD_STOP_LONG_BIAS = 0.12

TARGET_GR = 30

FUNDS_DICT = {}
HS_300 = {}
SHOULD_SELL_CODES = []
SHOULD_BUY_CODES = []
SHOULD_DAC_CODES = []

MAYBE_TOTAL = decimal.Decimal(0)

NEED_ANALYSIS = False
COLOR_FLAG = True
TODAY = time.strftime("%Y-%m-%d", time.localtime())
TW = time.localtime().tm_wday.numerator+1
TRADING_FLAG = None


def main():
    print(TODAY)
    print('--------------------------------------------------')
    repository.upsert_all()
    print('--------------------------------------------------')
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)
    global SPIDER_SLEEP
    global TARGET_GR
    global BASIC_STEP
    global BASIC_DAC_STEP
    global BASIC_BUILD_STEP
    global BASIC_BUILD_BIG_STEP
    global BASIC_GR
    global BAD_STOP_LONG_BIAS
    global GOOD_STOP_LONG_BIAS
    global FUNDS_DICT
    global SHOULD_SELL_CODES
    global SHOULD_BUY_CODES
    global SHOULD_DAC_CODES
    global MAYBE_TOTAL
    global NEED_ANALYSIS
    global COLOR_FLAG
    with open('conf/config.json', 'r', encoding='utf-8') as f:
        cfg = json.load(f)
        for fund_info in cfg['funds']:
            FUNDS_DICT[fund_info['code']] = fund_info

        # SPIDER_SLEEP = cfg['spider_sleep_time']
        BASIC_STEP = cfg['basic_step']
        BASIC_DAC_STEP = cfg['basic_dac_step']
        BASIC_BUILD_STEP = cfg['basic_build_step']
        BASIC_BUILD_BIG_STEP = cfg['basic_build_big_step']
        BASIC_GR = cfg['basic_gr']
        BAD_STOP_LONG_BIAS = cfg['bad_stop_long_bias']
        GOOD_STOP_LONG_BIAS = cfg['good_stop_long_bias']
        TARGET_GR = cfg['target_gr']

    get_information()
    if TRADING_FLAG is not None and not TRADING_FLAG:
        logging.info('本日非交易日')
        print_with_color('==========')
        print_with_color('本日非交易日')
        print_with_color('==========')
        return
    print_with_color('==========', MAYBE_TOTAL)
    print_with_color('==========', MAYBE_TOTAL)
    if MAYBE_TOTAL > decimal.Decimal(0):
        print_with_color('==========', MAYBE_TOTAL)
        print_with_color('今日预计盈利, {}元'.format(str(MAYBE_TOTAL)), MAYBE_TOTAL)
        print_with_color('==========', MAYBE_TOTAL)
    else:
        print_with_color('----------', MAYBE_TOTAL)
        print_with_color('今日预计亏损, {}元'.format(str(MAYBE_TOTAL.copy_abs())), MAYBE_TOTAL)
        print_with_color('----------', MAYBE_TOTAL)
    print_with_color('==========', MAYBE_TOTAL)
    print_with_color('==========', MAYBE_TOTAL)
    if NEED_ANALYSIS:
        for code in FUNDS_DICT:
            fund = FUNDS_DICT[code]
            if not fund.get('analysis', True) or fund.get('hold_amount', 0) <= 0:
                continue
            if time.localtime().tm_hour> 10 and time.localtime().tm_hour < 15:
                now = {
                    'date': TODAY,
                    'opt': fund['opt']
                }
                repository.upsert_logs(fund['code'], now)
            if fund['opt'] == '加仓' or fund['opt'] == '建仓':
                SHOULD_BUY_CODES.append(fund['code'])
            elif fund['opt'] == '减仓':
                SHOULD_SELL_CODES.append(fund['code'])
            elif fund['opt'] == '定投':
                SHOULD_DAC_CODES.append(fund['code'])

        if len(SHOULD_BUY_CODES) > 0:
            print_with_color('\n以下为买入建议')
            print_funds_opt_suggestion_info(SHOULD_BUY_CODES)

        if len(SHOULD_SELL_CODES) > 0:
            print_with_color('\n以下为卖出建议')
            print_funds_opt_suggestion_info(SHOULD_SELL_CODES)

        if len(SHOULD_DAC_CODES) > 0:
            print_with_color('\n以下为定投建议')
            print_funds_opt_suggestion_info(SHOULD_DAC_CODES)

        # print_with_color('\n')
        # print_with_color('\n')
        # print_with_color('\n')
        # print_with_color('\n')
        # if len(SHOULD_BUY_CODES) > 0 or len(SHOULD_DAC_CODES) > 0:
        #     print_with_color('\n以下为购买建议')
        #     if len(SHOULD_BUY_CODES) > 0:
        #         print_funds_opt_suggestion_simple(SHOULD_BUY_CODES)
        #         print_with_color('\n\n')
        #     if len(SHOULD_DAC_CODES) > 0:
        #         print_funds_opt_suggestion_simple(SHOULD_DAC_CODES)
        #         print_with_color('\n\n')



        # print_with_color('计算售出份额[份额=希望卖出金额/净值], \'n\'或者\'N\'可以跳过')
        # print_with_color('建议止盈={}%，建议止损={}%'.format(str(STOP_PROFIT_DECIMAL), str(STOP_LOSS_DECIMAL)))
        # while True:
        #     code = input('请输入基金编号=')
        #     if code == 'n' or code == 'N':
        #         break
        #     if code in FUNDS_DICT:
        #         fund = FUNDS_DICT[code]
        #         fund_full_name = '【{}:{}】'.format(fund['code'], fund['name'])
        #         for info in fund['info']:
        #             print_with_color(info)
        #         wa = input('请输入希望卖出{}的金额='.format(fund_full_name))
        #         sell_share = (decimal.Decimal(wa) / fund['npv']).quantize(decimal.Decimal('0.00'),
        #                                                                   decimal.ROUND_HALF_UP)
        #         res = "售出 {} 份".format(str(sell_share))
        #         print_with_color('{} 建议 {}'.format(fund_full_name, res))
        #         print_with_color('')


def print_funds_opt_suggestion_simple(codes):
    for code in codes:
        fund = FUNDS_DICT[code]
        print_with_color(fund['fullname'], fund['lgr'])
        print_with_color(opt_result_format.format(fund['opt'], fund['opt_result']), fund['lgr'])

def print_funds_opt_suggestion_info(codes):
    for code in codes:
        fund = FUNDS_DICT[code]
        print_opt_suggestion_info(fund, True)
        print_with_color('==========')


def print_opt_suggestion_info(fund, need_analysis=False):
    print_with_color(fund['fullname'], fund['lgr'])
    if 'predicate' in fund:
        print_with_color('预计收益:{}元'.format(str(fund['predicate'])), fund['predicate'])
    print_with_color(fund['late'], fund['lgr'])
    if need_analysis:
        print_with_color('[' + fund['long_trend_status'] + '] ' + fund['analysis_information'], fund['lgr'])
        print_with_color(fund['day_5_ga'], fund['lgr'])
        print_with_color(fund['bias_information'], fund['lgr'])

        for item in fund['suggestion']:
            print_with_color(item, fund['lgr'])

        logs = fund.get('logs', [])
        if len(logs) > 0:
            log_info_list = []
            for log in logs:
                log_info_list.append(log['date'] + ':' + log['opt'])
            print_with_color('操作日志: ' + ', '.join(log_info_list))

        if fund['opt'] != '-':
            print_with_color(opt_result_format.format(fund['opt'], fund['opt_result']), fund['lgr'])



def get_information():
    global MAYBE_TOTAL
    global FUNDS_DICT
    global NEED_ANALYSIS
    # 沪深300 信息
    # HS_300 = spider.get_stock_info('sz399300')
    # HS_300['histories'] = spider.get_stock_history('zs_399300')

    for code in FUNDS_DICT:
        try:
            sleep_time = 0.5 + random.random()
            logging.info('sleep {:.2f}s'.format(sleep_time))
            time.sleep(sleep_time)

            fund = FUNDS_DICT[code]
            fund_late_info = spider.get_fund_info(code)
            if not TRADING_FLAG:
                break
            fund.update(fund_late_info)

            build_complete = fund.get('build_complete', False)
            hold_amount = fund.get('hold_amount', 0)
            if hold_amount > 0:
                this_maybe = (fund['lgr'] * decimal.Decimal(hold_amount) / decimal.Decimal(100))
                MAYBE_TOTAL = MAYBE_TOTAL + this_maybe
                fund['predicate'] = this_maybe
            if build_complete:
                build_cost = decimal.Decimal(fund.get('build_cost', 1.0000))
                target_gr = decimal.Decimal(TARGET_GR)

                rate_target_complete = (
                            (fund['lnpv'] - build_cost) / build_cost * decimal.Decimal(10000) / target_gr).quantize(decimal.Decimal('0.00'), decimal.ROUND_HALF_UP)

                fund['rate_target_complete'] = rate_target_complete
                fund['fullname'] = fund['fullname'] + ' (止盈进度{}%'.format(fund['rate_target_complete'])
                target_complete = fund.get('target_complete', 0)
                if target_complete > 0:
                    fund['fullname'] = fund['fullname'] + ', 已止盈{}次'.format(str(target_complete))
                fund['fullname'] = fund['fullname'] + ')'
            else:
                fund['fullname'] = fund['fullname'] + ' (建仓进度{}%)'.format(
                    str((hold_amount / decimal.Decimal(10)).quantize(decimal.Decimal('0.00'), decimal.ROUND_HALF_UP)))

            fund['info'] = []
            fund['suggestion'] = []

            if NEED_ANALYSIS:
                fund['histories'] = repository.get_histories(code)
                fund['logs'] = repository.get_logs(code, TODAY)
                analysis.analysis_fund(fund)
                fund['fullname'] = fund['fullname']
            FUNDS_DICT[code] = fund
            print_opt_suggestion_info(fund, NEED_ANALYSIS)

            print_with_color('')
        except:
            logging.ERROR("{} analysis error".format(code))
            pass


def print_with_color(info, color=0):
    global COLOR_FLAG
    if COLOR_FLAG and color < 0:
        print('\033[1;32m {}\033[0m'.format(info))

    elif COLOR_FLAG and color > 0:
        print('\033[1;31m {}\033[0m'.format(info))

    else:
        print(' {}'.format(info))


if __name__ == '__main__':
    now_hour = time.localtime().tm_wday
    print(str(now_hour.numerator))
    print(time.strftime("%Y-%m-%d", time.localtime()))

    # start = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    # main()
    # end = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    # print('query time:')
    # print('{}~{}'.format(start, end))
