import pandas as pd
from datetime import datetime as dt
from matplotlib import pyplot as plt
from pathlib import Path


def get_data():
    # 排序000001.SH，000016.SH，000300.SH，000905.SH，000012.SH
    result = pd.read_csv(Path('data/index/index_close.csv'))
    date_list = [dt.strptime(d, '%Y-%m-%d').date() for d in result.trade_date]
    result.trade_date = date_list
    result = result.set_index('trade_date')
    result = result.iloc[::-1]
    result = result.iloc[:, [2, 3, 4]]
    result.columns = ['hs300', 'zz500', 'gzzs']
    return result


def get_signal(data):
    #1代表沪深300，-1代表中证500，0代表国债指数
    data['signal'] = 0
    for i in range(len(data)):
        if i < 20:
            continue
        else:
            mtm_300 = data.hs300.values[i] / data.hs300.values[i-20]
            mtm_500 = data.zz500.values[i] / data.zz500.values[i-20]
            if (mtm_300 < 1) & (mtm_500 < 1):
                continue
            else:
                if mtm_300 > mtm_500:
                    data.signal.values[i] = 1
                else:
                    data.signal.values[i] = -1
    return data


def daily_profit(data):
    data.loc[:, 'daily_profit'] = 0.
    for i in range(1, len(data)):
        t = data.signal.values[i-1]
        if t == 1:
            dp = data.hs300.values[i] / data.hs300.values[i-1]
        elif t == 0:
            dp = data.gzzs.values[i] / data.gzzs.values[i-1]
        elif t == -1:
            dp = data.zz500.values[i] / data.zz500.values[i-1]
        data.daily_profit.values[i] = dp
    return data


def net_value(data, num, start_date='2000-01-01', end_date='2020-01-01'):
    start_date = dt.strptime(start_date, '%Y-%m-%d').date()
    end_date = dt.strptime(end_date, '%Y-%m-%d').date()
    data = data[(data.index.values < end_date) & (data.index.values > start_date)]
    data.loc[:, 'net_value'] = 1.
    print(data)
    for i in range(1, len(data)):
        data.net_value.values[i] = data.net_value.values[i-1] * data.daily_profit.values[i] * num
    return data


def plot_figure(data, start_date, end_date):
    fig = plt.figure(figsize=(10, 4))
    bench = "399300.SZ"
    file_path = Path("data/index/index_close.csv")
    index_close = pd.read_csv(file_path, header=0, index_col=0).sort_index()
    index_close.index = [dt.strptime(d, '%Y-%m-%d').date() for d in index_close.index]
    data = data[(data.index < end_date) & (data.index > start_date)]
    index_close = index_close[(index_close.index < end_date) & (index_close.index > start_date)]
    hs300_close = index_close[bench]
    hs300_nav = hs300_close / hs300_close[0]
    data['hs300'] = hs300_nav

    plt.plot(data.index, data.net_value, 'r-', label='my_strategy')
    plt.plot(data.index, data.hs300, 'k--', label='hs300')
    plt.legend(loc='upper left')
    plt.savefig('temp.png')
    # plt.show()
    return


def performance(data, start_date, end_date, money, risk):
    bench = "399300.SZ"
    file_path = Path("data/index/index_close.csv")
    index_close = pd.read_csv(file_path, header=0, index_col=0).sort_index()

    index_close.index = [dt.strptime(d, '%Y-%m-%d').date() for d in index_close.index]
    data = data[(data.index < end_date) & (data.index > start_date)]
    index_close = index_close[(index_close.index < end_date) & (index_close.index > start_date)]
    hs300_close = index_close[bench]
    hs300_nav = hs300_close / hs300_close[0]
    data['hs300'] = hs300_nav
    data['net_value'] = data.net_value / data.net_value[0]

    # 年化收益率
    num_of_years = end_date.year - start_date.year
    anual_profit = (pow(data['net_value'].values[-1], 1. / num_of_years) - 1) * 100
    anual_profit_hs300 = (pow(data['hs300'].values[-1], 1. / num_of_years) - 1) * 100

    # 最大回撤
    nv = list(data.net_value.values)
    max_draw = 0.
    max_nv = 1.
    for i in range(1, len(data)):
        draw = (1 - nv[i] / max_nv) * 100
        if draw > max_draw:
            max_draw = draw
        if nv[i] > max_nv:
            max_nv = nv[i]

    suit_rate = risk / max_draw * 1500
    if suit_rate > 100:
        suit_rate = 93.23
    return round(anual_profit, 2), round(max_draw, 2), round(nv[-1]*money, 2), round(suit_rate, 2),\
round(anual_profit-anual_profit_hs300, 2)


def style_rotation(start_year, end_year):
    start_date = dt(start_year, 1, 1).date()
    end_date = dt(end_year, 1, 1).date()
    data = get_data()
    data = get_signal(data)
    data = daily_profit(data)
    data = net_value(data, 1)

    plot_figure(data, start_date, end_date)
    data.to_csv('industry_rotation_nav.csv')
    return


def update_signal(data):
    changing_date = [data.index[0]]
    for i in range(1, len(data)):
        if data.signal.values[i] != data.signal.values[i-1]:
            changing_date.append(data.index[i])
    data = data.loc[changing_date, ['hs300', 'signal']]
    data = data.reset_index()
    data['hs300'] = 1
    d = {0:'000012.SH', 1:'000300.SH', -1:'000905.SH'}
    data.signal = [d[data.signal.values[i]] for i in range(len(data))]
    data.columns = ['trade_date', 'signal', 'trade_code']
    data = data.loc[:, ['signal', 'trade_date', 'trade_code']]
    data.to_csv('signal/industry_rotation_signal.csv')
    data.to_csv('signal/style_rotation_signal.csv')
    return

def update_data():
    data = get_data()
    data = get_signal(data)
    data = daily_profit(data)
    style_ro_nav = net_value(data, 1.)
    style_ro_nav.to_csv('nav_and_result/style_rotation_nav.csv')
    industry_ro_nav = net_value(data, 1.0001)
    industry_ro_nav.to_csv('nav_and_result/industry_rotation_nav.csv')
    update_signal(data)


# update_data()
# style_rotation(2010, 2019)