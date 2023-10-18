# coding=utf8
import decimal
import logging
import time

import leek_analysis

basic_res_format = '趋势为【{}】，60日均值={}元，30日均值={}元, 净值={}元， 预测净值={}元'
day_res_format = '【{}日指标】:bias={}%，late_bias={}%, min={}元, max={}元， avg={}元'
suggestion_format = '【建议{}】因为: {}'
bias_suggestion_opt_format = '【{}BIAS定投建议】{}'
analysis_information_format = '60日净值区间[{}, {}], 平均{}元, Y({})={}%'
bias_information_format = '偏离率: Y(5)={}%, Y(10)={}%, Y(30)={}%, Y({})={}%'
day_5_ga_prefix = '5日预计涨幅: '


def analysis_fund(fund):
    fund['compute_index'] = {}
    fund['compute_lgr'] = {}
    if 'histories' in fund:
        npv_min = fund['npv']
        npv_max = fund['npv']
        npv_total = decimal.Decimal(0)
        lnpv_total = fund['lnpv']
        range_max = len(fund['histories'])
        if len(fund['histories']) >= 250:
            range_max = 250

        for index in range(range_max):
            item = fund['histories'][index]
            that_day_npv = decimal.Decimal(item['npv'])
            npv_total += that_day_npv
            if that_day_npv > npv_max:
                npv_max = that_day_npv
            if that_day_npv < npv_min:
                npv_min = that_day_npv
            day = index + 1
            if day == 5 or day == 10 or day == 30 or day == 60 or day == 250 or day == range_max:
                fund['compute_index'][str(day)] = index_handle(fund, npv_total, lnpv_total, npv_min, npv_max,
                                                               decimal.Decimal(day))
            if day <= 5:
                fund['compute_lgr'][str(day)] = lgr_handle(fund['lnpv'],
                                                           decimal.Decimal(fund['histories'][index]['npv']))

            lnpv_total += that_day_npv
        fund['npv_min'] = npv_min
        fund['npv_max'] = npv_max
    else:
        logging.error('{}-{} has no histories, it cannot be analysis!'.format(fund['code'], fund['name']))

    fund['opt'] = '-'

    index_60 = '60'
    if len(fund['histories']) < 60:
        index_60 = str(len(fund['histories']))
    npv_avg_60 = fund['compute_index'][index_60]['npv_avg']
    npv_min_60 = fund['compute_index'][index_60]['npv_min']
    npv_max_60 = fund['compute_index'][index_60]['npv_max']
    index_30 = '30'
    if len(fund['histories']) < 30:
        index_30 = str(len(fund['histories']))
    npv_avg_30 = fund['compute_index'][index_30]['npv_avg']
    bais_30 = fund['compute_index'][index_30]['bias']
    lbias_30 = fund['compute_index'][index_30]['lbias']

    index_10 = '10'
    if len(fund['histories']) < 10:
        index_10 = str(len(fund['histories']))
    bais_10 = fund['compute_index'][index_10]['bias']
    lbias_10 = fund['compute_index'][index_10]['lbias']
    npv_min_10 = fund['compute_index'][index_10]['npv_min']

    index_5 = '5'
    if len(fund['histories']) < 5:
        index_5 = str(len(fund['histories']))
    bais_5 = fund['compute_index'][index_5]['bias']
    lbias_5 = fund['compute_index'][index_5]['lbias']

    long_trend_status = '平稳'  # 长期走势  下跌  平稳  上涨
    stop_bias = (decimal.Decimal(leek_analysis.GOOD_STOP_LONG_BIAS) + decimal.Decimal(
        leek_analysis.BAD_STOP_LONG_BIAS)) / decimal.Decimal(2)
    if npv_avg_60 < npv_avg_30:
        # 30日均值 > 60日均值，行情看好
        long_trend_status = '上涨'
        stop_bias = decimal.Decimal(leek_analysis.GOOD_STOP_LONG_BIAS)
    elif npv_avg_60 > npv_avg_30:
        # 30日均值 < 60日均值，行情不看好
        long_trend_status = '下跌'
        stop_bias = decimal.Decimal(leek_analysis.BAD_STOP_LONG_BIAS)

    fund['long_trend_status'] = long_trend_status

    # 定投建议
    if len(fund['histories']) < 250:
        dac_day = str(len(fund['histories']))
    else:
        dac_day = str(250)
    bias = (fund['compute_index'][dac_day]['lbias'] / 100).quantize(decimal.Decimal('0.0000'), decimal.ROUND_HALF_UP)
    long_bias_str = str(bias * decimal.Decimal(100))
    day_5_ga_str = day_5_ga_prefix
    for index in range(5):
        day_5_ga_str = day_5_ga_str + 'day[{}]={}%, '.format(str(index + 1), fund['compute_lgr'][str(index + 1)])
    fund['day_5_ga'] = day_5_ga_str
    fund['bias_information'] = bias_information_format.format(str(lbias_5), str(lbias_10), str(lbias_30), dac_day,
                                                              long_bias_str)
    fund['analysis_information'] = analysis_information_format.format(str(npv_min_60), str(npv_max_60), str(npv_avg_60),
                                                                      dac_day, long_bias_str)

    fund['opt'] = '-'
    lb_m = decimal.Decimal(1)
    if fund['lgr'] >= 0 and fund.get('hold_amount', 0) > 0:
        # 卖出逻辑
        if lbias_30 >= decimal.Decimal(16) or bais_30 >= decimal.Decimal(16):
            fund['opt'] = '减仓'
            fund['suggestion'].append(
                suggestion_format.format(fund['opt'], '30日乖离率达到16%, lbias_30={}%'.format(lbias_30)))
            lb_m = lb_m + (lbias_30 / 10).copy_abs()
        elif lbias_10 >= decimal.Decimal(8) or bais_10 >= decimal.Decimal(8):
            fund['opt'] = '减仓'
            fund['suggestion'].append(
                suggestion_format.format(fund['opt'], '10日乖离率达到8%, lbias_10={}%'.format(lbias_10)))
            lb_m = lb_m + (lbias_10 / 10).copy_abs()
        elif lbias_5 >= decimal.Decimal(5) or bais_5 >= decimal.Decimal(5):
            fund['opt'] = '减仓'
            fund['suggestion'].append(suggestion_format.format(fund['opt'], '5日乖离率达到5%, lbias_5={}%'.format(lbias_5)))
            lb_m = lb_m + (lbias_5 / 10).copy_abs()
        # 收益不理想，看空模式
        if fund['lgr'] >= (decimal.Decimal(leek_analysis.BASIC_GR) * decimal.Decimal(0.25)) and ((fund.get(
                'analysis', True) and fund.get('rate_target_complete', 0) < decimal.Decimal(-10) and fund.get(
                'long_trend_status', '平稳') == '下跌') or fund.get('type', 'normal') == 'short'):
            # 看空模式，涨点就卖
            algr_flag = (decimal.Decimal(leek_analysis.BASIC_GR * decimal.Decimal(1)))
            algr_step = (decimal.Decimal(leek_analysis.BASIC_GR * decimal.Decimal(0.125)))
            lgr_suggestions = []
            for index in range(5):
                algr = fund['compute_lgr'][str(index + 1)]
                if algr > (algr_flag + (algr_step * index)):
                    fund['opt'] = '减仓'
                    lgr_suggestions.append(
                        suggestion_format.format(fund['opt'], '预计{}日涨幅达到{}%'.format(str(index + 1), algr)))
            if len(lgr_suggestions) > 0:
                fund['suggestion'].append(lgr_suggestions[len(lgr_suggestions) - 1])
            npm_midd = ((fund['npv_min'] + fund['npv_max']) / decimal.Decimal(2)).quantize(decimal.Decimal('0.0000'),
                                                                                           decimal.ROUND_HALF_UP)
            if npm_midd <= fund['lnpv'] and fund['lgr'] >= decimal.Decimal(leek_analysis.BASIC_GR):
                fund['opt'] = '减仓'
                fund['suggestion'].append(
                    suggestion_format.format(fund['opt'], '超过{}天净值中间值{}'.format(dac_day, npm_midd)))
            if npv_avg_60 <= fund['lnpv']  and fund['lgr'] >= decimal.Decimal(leek_analysis.BASIC_GR):
                fund['opt'] = '减仓'
                fund['suggestion'].append(
                    suggestion_format.format(fund['opt'], '超过60天净值均值{}'.format(npv_avg_60)))

        # 目标达成
        if fund.get('rate_target_complete', 0) > decimal.Decimal(100):
            fund['opt'] = '减仓'
            fund['suggestion'].append(
                suggestion_format.format(fund['opt'], '达到止盈目标'))

    elif fund['lgr'] < leek_analysis.BASIC_GR * decimal.Decimal(-0.25):
        # 买入逻辑
        if lbias_30 <= decimal.Decimal(-16) or bais_30 <= decimal.Decimal(-16):
            fund['opt'] = '加仓'
            fund['suggestion'].append(
                suggestion_format.format(fund['opt'], '30日乖离率达到-16%, lbias_30={}%'.format(lbias_30)))
            lb_m = lb_m + (lbias_30 / 10).copy_abs()
        elif lbias_10 <= decimal.Decimal(-8) or bais_10 <= decimal.Decimal(-8):
            fund['opt'] = '加仓'
            fund['suggestion'].append(
                suggestion_format.format(fund['opt'], '10日乖离率达到-8%, lbias_10={}%'.format(lbias_10)))
            lb_m = lb_m + (lbias_10 / 10).copy_abs()
        elif lbias_5 <= decimal.Decimal(-5) or bais_5 <= decimal.Decimal(-5):
            fund['opt'] = '加仓'
            fund['suggestion'].append(suggestion_format.format(fund['opt'], '5日乖离率达到-5%, lbias_5={}%'.format(lbias_5)))
            lb_m = lb_m + (lbias_5 / 10).copy_abs()
        elif fund['lgr'] <= leek_analysis.BASIC_GR * decimal.Decimal(-1) and (
                fund.get('hold_amount', 0) == 0 or not fund.get('build_complete', False)):
            if lbias_30 <= decimal.Decimal(-12.8) or bais_30 <= decimal.Decimal(-12.8):
                fund['opt'] = '建仓'
                fund['suggestion'].append(
                    suggestion_format.format('建仓', '30日乖离率达到-12.8%, lbias_30={}%'.format(lbias_30)))
            elif lbias_10 <= decimal.Decimal(-6.4) or bais_10 <= decimal.Decimal(-6.4):
                fund['opt'] = '建仓'
                fund['suggestion'].append(
                    suggestion_format.format('建仓', '10日乖离率达到-6.4%, lbias_10={}%'.format(lbias_10)))
            elif lbias_5 <= decimal.Decimal(-4) or bais_5 <= decimal.Decimal(-4):
                fund['opt'] = '建仓'
                fund['suggestion'].append(suggestion_format.format('建仓', '5日乖离率达到-4%, lbias_5={}%'.format(lbias_5)))

        if fund.get('hold_amount', 0) > 0:
            algr_flag = (decimal.Decimal(leek_analysis.BASIC_GR) * decimal.Decimal(-1))
            algr_step = (decimal.Decimal(leek_analysis.BASIC_GR) * decimal.Decimal(-0.5))
            # 看空模式，降低加仓门槛
            if fund.get('analysis', True) and fund.get('rate_target_complete', 0) < decimal.Decimal(-10) and fund.get(
                    'long_trend_status', '平稳') == '下跌':
                algr_flag = (decimal.Decimal(leek_analysis.BASIC_GR) * decimal.Decimal(-0.75))
                algr_step = (decimal.Decimal(leek_analysis.BASIC_GR) * decimal.Decimal(-0.125))
            lgr_suggestions = []
            for index in range(5):
                algr = fund['compute_lgr'][str(index + 1)]
                if algr < (algr_flag + (algr_step * index)):
                    if fund['opt'] == '-':
                        fund['opt'] = '加仓'
                    lgr_suggestions.append(
                        suggestion_format.format(fund['opt'], '预计{}日跌幅达到{}%'.format(str(index + 1), algr)))
            if len(lgr_suggestions) > 0:
                fund['suggestion'].append(lgr_suggestions[len(lgr_suggestions) - 1])

        # if (fund['opt'] == '加仓' or fund['opt'] == '建仓') and fund['lnpv'] < npv_min_10:
        if (fund['opt'] == '加仓' or fund['opt'] == '建仓'):
            range_max = len(fund['histories'])
            if len(fund['histories']) >= 250:
                range_max = 250

            for index in range(1, range_max):
                item = fund['histories'][index]
                that_day_npv = decimal.Decimal(item['npv'])
                if fund['lnpv'] >= that_day_npv:
                    fund['suggestion'].append(
                        suggestion_format.format(fund['opt'], '预计达到{}日内最低值'.format(str(index + 1))))
                    break
            # fund['suggestion'].append(suggestion_format.format(fund['opt'], '预计达到60日内最低值'))
        if fund['lnpv'] < npv_min:
            fund['suggestion'].append('【WARNING】预计达到记录历史新低')
            if fund.get('hold_amount', 0) > 0:
                fund['opt'] = '加仓'

        if fund.get('rate_target_complete', 0) >= 80 and index > 10:
            val = (decimal.Decimal(1) - (lbias_5 * decimal.Decimal(0.2)) - (
                    lbias_10 * decimal.Decimal(0.1)) - (
                           lbias_30 * decimal.Decimal(0.03))) * decimal.Decimal(leek_analysis.BASIC_BUILD_BIG_STEP)
            val = val.quantize(decimal.Decimal('0'), decimal.ROUND_HALF_UP)
            fund['suggestion'].append('【建仓】建议买入 {}元建仓(basic={})'.format(str(val), str(leek_analysis.BASIC_BUILD_BIG_STEP)))
        if (fund['opt'] == '加仓' or fund['opt'] == '建仓') and not fund.get('build_complete', False):
            val = (decimal.Decimal(1) - (lbias_5 * decimal.Decimal(0.2)) - (lbias_10 * decimal.Decimal(0.1)) - (
                    lbias_30 * decimal.Decimal(0.03))) * decimal.Decimal(leek_analysis.BASIC_BUILD_STEP)
            val = val.quantize(decimal.Decimal('0'), decimal.ROUND_HALF_UP)
            fund['suggestion'].append('【建仓】建议买入 {}元建仓(basic={})'.format(str(val), str(leek_analysis.BASIC_BUILD_STEP)))

    basic = decimal.Decimal(leek_analysis.BASIC_STEP)
    t = (decimal.Decimal(-1) / stop_bias).quantize(decimal.Decimal('0.00'), decimal.ROUND_HALF_UP)
    val = ((bias * (decimal.Decimal(-1) / stop_bias) + 1) * basic).quantize(decimal.Decimal('0.00'),
                                                                            decimal.ROUND_HALF_UP)

    if val >= 0:
        opt_result = '买入{}元(basic={}, t={}, lb_m={})'.format(str(val), str(basic), str(t), str(lb_m))
    elif val < 0:
        opt_result = '卖出{}元(basic={}, t={}, lb_m={})'.format(str(val.copy_abs()), str(basic), str(t), str(lb_m))

    if logs_analysis_dac(fund):
        fund['opt'] = '定投'

    logs_analysis_add(fund)

    if (fund['opt'] == '加仓' or fund['opt'] == '定投' or fund['opt'] == '建仓') and val < 0:
        opt_result = '最低买入10元, ' + opt_result
    elif fund['opt'] == '减仓' and val >= 0:
        opt_result = '最低卖出10份, ' + opt_result

    fund['opt_result'] = opt_result
    fund['late'] = fund['late'] + ', {}天净值区间[{},{}]'.format(str(len(fund['histories'])), str(fund['npv_min']),
                                                            str(fund['npv_max']))


def logs_analysis_dac(fund):
    if fund.get('hold_amount', 0) <= 0 or fund['opt'] != '-' or not fund.get('dac', True):
        return False
    if leek_analysis.TW == 1 and fund['lgr'] > decimal.Decimal(-1.0):
        return False
    if leek_analysis.TW == 2 and fund['lgr'] > decimal.Decimal(-0.75):
        return False
    if leek_analysis.TW == 3 and fund['lgr'] > decimal.Decimal(-0.5):
        return False
    if leek_analysis.TW == 4 and fund['lgr'] > decimal.Decimal(-0.25):
        return False
    if leek_analysis.TW == 5 and fund['lgr'] > decimal.Decimal(0):
        return False
    logs = fund.get('logs', [])
    if len(logs) < 5:
        return False
    for log_index in range(0, leek_analysis.TW):
        if is_buy(logs[log_index]):
            return False
    return True


def logs_analysis_add(fund):
    if fund.get('hold_amount', 0) <= 0 or fund['opt'] != '-':
        return
    logs = fund.get('logs', [])
    if len(logs) == 0:
        return
    log = logs[0]
    if fund['lgr'] <= - 1 and is_buy(log):
        fund['opt'] = log.get('opt', '-')
        fund['suggestion'].append(suggestion_format.format(fund['opt'], '追加上日操作'))
        return


def index_handle(fund, npv_total, lnpv_total, npv_min, npv_max, day):
    res = {}
    npv = fund['npv']
    lnpv = fund['lnpv']
    npv_avg = (npv_total / decimal.Decimal(day)).quantize(decimal.Decimal('0.0000'), decimal.ROUND_DOWN)
    bias = ((npv - npv_avg) * decimal.Decimal(100) / npv_avg).quantize(decimal.Decimal('0.00'), decimal.ROUND_DOWN)
    lnpv_avg = (lnpv_total / decimal.Decimal(day)).quantize(decimal.Decimal('0.0000'), decimal.ROUND_DOWN)
    lbias = ((lnpv - lnpv_avg) * decimal.Decimal(100) / lnpv_avg).quantize(decimal.Decimal('0.00'), decimal.ROUND_DOWN)
    res['npv_min'] = npv_min
    res['npv_max'] = npv_max
    res['npv_avg'] = npv_avg
    res['bias'] = bias
    res['lnpv_avg'] = lnpv_avg
    res['lbias'] = lbias
    return res


def lgr_handle(lnpv, npv):
    return ((lnpv - npv) / npv * 100).quantize(decimal.Decimal('0.00'), decimal.ROUND_HALF_UP)


def is_number(s):
    '''
    判断字符串是否是数字
    :param s:
    :return:
    '''
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def funds_sort(codes, reverse=False):
    codes.sort(key=get_lgr(), reverse=reverse)
    return codes


def get_lgr(code):
    return leek_analysis.FUNDS_DICT[code]['lgr']


def is_buy(log):
    opt = log.get('opt', '-')
    if opt == '加仓' or opt == '建仓' or opt == '定投':
        return True
    return False


def yesterday_is_buy(fund):
    logs = fund.get('logs', [])
    if len(logs) == 0:
        return False
    return is_buy(logs[0])
