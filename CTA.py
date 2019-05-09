
import matplotlib.pyplot as plt
import pandas as pd
#import tushare as ts
import math
from datetime import datetime, date, timedelta
from pathlib import  Path


def DT(data, N, K1, K2, asset,min_change,margin_rate,asset_rate,price,target):
    # 获取数据
    #price = 300  # 每点多少钱
    #min_change = 0.05  # 最少买进的合约数目
    #margin_rate = 0.12  # 保证金比率
    #asset_rate = 0.5  # 资金使用量
    data = data.set_index('trade_date')
    df = pd.DataFrame()  # 创建新DataFrame
    df['close'] = data['close'] * price  # 收盘价
    df["low"] = data["low"] * price  # 最低价
    df["high"] = data["high"] * price  # 最高价
    df["open"] = data["open"] * price
    df['change'] = data['close'] - data['close'].shift(1)  # 每日收盘价的变动

    # 计算HH,HC,LL,LC
    df["range"] = 0
    df["HH"] = df["high"].rolling(window=N, center=False).max()
    df["HC"] = df["close"].rolling(window=N, center=False).max()
    df["LC"] = df["close"].rolling(window=N, center=False).min()
    df["LL"] = df["low"].rolling(window=N, center=False).min()
    df = df.dropna()
    date = df.index
    print(date)
    date = pd.to_datetime([str(i) for i in date])
    df.index = [i for i in range(len(df.index))]

    for i in range(len(df.index)):
        df['range'][i] = max((df['HH'][i] - df['LC'][i]), (df['HC'][i] - df['LL'][i]))
    df['range'] = df['range'].shift(1)
    df["buyline"] = df["open"] + K1 * df["range"]
    df["sellline"] = df["open"] - K2 * df["range"]

    #     plt.figure()
    #     #x = pd.to_datetime(df.index[pd.to_datetime(df.index)>datetime(2018,8,1)])
    #     #plt.plot(x,df["close"][pd.to_datetime(df.index)>datetime(2018,8,1)],color = "blue",label = "close")
    #     #plt.plot(x,df["buyline"][pd.to_datetime(df.index)>datetime(2018,8,1)],color = "red",label = "buyline")
    #     #plt.plot(x,df["sellline"][pd.to_datetime(df.index)>datetime(2018,8,1)],color = "green",label = "sellline")
    #     plt.plot(date,df['close'])
    #     plt.xlabel('date')
    #     plt.ylabel('Price(Yuan/Ton)')
    #     plt.legend()
    #     plt.xticks(rotation = 45)
    #     plt.show()
    def fee(n):
        return (df['pos'][n] - df['pos'][n - 1]) * df['open'][n] * 3 / 10000

    def close_position(n):
        return df['pos'][n - 1] * (df['open'][n] - df['close'][n - 1])

    df['pos'] = 0  # 仓位
    df['signal'] = 0  # 交易信号
    df['profit'] = 0  # 当期盈亏
    df['fee'] = 0  # 手续费
    global inprice  # 入场价格
    # 信号判断
    inprice = 0
    for m in range(1, len(df.index) - 1):
        if abs(df['close'][m] - inprice) > inprice * 0.02 and df['pos'][m] != 0:  # 止损条件
            df['signal'].iloc[m] = -2
            df['pos'].iloc[m + 1] = 0
            df['fee'].iloc[m + 1] = fee(m + 1)
            df['profit'].iloc[m + 1] = close_position(m + 1)
        elif (df['close'][m] > df['buyline'][m] and df['close'][m - 1] < df['buyline'][m - 1]):  # 上穿
            if df['pos'][m] > 0:
                df['pos'].iloc[m + 1] = df['pos'].iloc[m]
            else:
                df['signal'].iloc[m] = 1
                inprice = df['open'][m + 1]
                df['pos'].iloc[m + 1] = int(asset * asset_rate / (df['open'][m + 1] * min_change * margin_rate)) * min_change
                df['fee'].iloc[m + 1] = fee(m + 1)
                df['profit'].iloc[m + 1] = df['pos'][m + 1] * (df['close'][m + 1] - df['open'][m + 1]) + df['pos'][m + 1] * abs(df['close'][m + 1] - df['open'][m + 1]) * 0.5 + close_position(m + 1)
        elif (df['close'][m] < df['sellline'][m] and df['close'][m - 1] > df['sellline'][m - 1]):  # 下穿
            if df['pos'][m] < 0:
                df['pos'].iloc[m + 1] = df['pos'].iloc[m]
            else:
                df['signal'].iloc[m] = -1
                inprice = df['open'][m + 1]
                df['pos'].iloc[m + 1] = -int(
                    asset * asset_rate / (df['open'][m + 1] * min_change * margin_rate)) * min_change
                df['fee'].iloc[m + 1] = fee(m + 1)
                df['profit'].iloc[m + 1] = df['pos'].iloc[m + 1] * (df['close'][m + 1] - df['open'][m + 1]) + df['pos'][
                    m + 1] * abs(df['close'][m + 1] - df['open'][m + 1]) * 0.3 + close_position(m + 1)
        else:  # 没有信号
            df['pos'].iloc[m + 1] = df['pos'].iloc[m]
            df['profit'].iloc[m + 1] = df['pos'].iloc[m + 1] * df['change'].iloc[m + 1]
    df['netpnl'] = df['profit'] - df['fee']  # 净盈亏
    df['plt'] = (df['netpnl'].cumsum()+asset)
    df['cumpnl'] = (df['netpnl'].cumsum()+ asset)/asset  # 累计盈亏 cumsum（）
    signal = pd.DataFrame(columns = ['signal','trade_date','trade_code'])
    signal['trade_date'] = date.values
    signal['signal'] = df['signal'].values
    #print (signal['signal'])
    #signal['asset_rate'] = asset_rate
    signal['trade_code'] = target
    signal = signal[signal['signal'] != 0]
    signal['signal'][signal['signal'] == 1] = asset_rate
    signal['signal'][signal['signal'] == -1] = -1* asset_rate
    signal['signal'][signal['signal'] == -2] = 0
    signal.index  = [k for k in range(len(signal.index))]

    result  = pd.DataFrame(index =  date, columns = ['net_value'])
    result['net_value'] = df['cumpnl'].values
    result.index.name =  'trade_date'

    plt.figure()
    plt.plot(date, df["plt"])
    plt.xlabel("date")
    plt.ylabel("Net Value")
    plt.xticks(rotation=45)
    plt.savefig(target+ str(N) + '_' + str(K1) + '_' + str(K2)+'.png')

    return result,signal

def getfuturesdata(target):
    address = Path(target+'.csv')
    data = pd.read_csv(address,index_col = 0)
    print(data)
    return data
def period(data, start_date,end_date):
    if int(start_date) not in data.index:
        time = datetime.strptime(start_date, '%Y%m%d').date()
        yesterday = (time + timedelta(days = -1)).strftime('%Y%m%d')
        j = 2
        while (int(yesterday) not in data.index) :
            yesterday = (time + timedelta(days = -j)).strftime('%Y%m%d')
            j = j + 1
            if int(yesterday) < data.index.min():
                print (start_date, 'is out of the date')
                break
        start_date = yesterday
    if int(end_date) not in data.index:
        time = datetime.strptime(end_date, '%Y%m%d').date()
        tommarow = (time + timedelta(days = 1)).strftime('%Y%m%d')
        j = 2
        while (int(tommarow) not in data.index) :
            tommarow= (time + timedelta(days = j)).strftime('%Y%m%d')
            j = j + 1
            if int(tommarow) > data.index.max():
                print (end_date, 'is out of the date')
                break
        end_date = tommarow
    print (start_date)
    print (end_date)
    selected_data = pd.DataFrame(data.loc[int(start_date):int(end_date)])
    return selected_data
# 获取数据IF.CFX
#def select
#trade_code = ['CF_ZCE','',]


#end_date = '20190410'
#数据预处理
def cta():
    # data  = data.set_index('trade_date')
    # start_date =  str(data.index[0])
    # end_date =  str(data.index[-1])
    # selected_data = period(data,start_date,end_date)
    profit1, signal1= DT(getfuturesdata('data/futures/SR_ZCE'),10,0.1,0.1,100000,10,0.08,0.5,1,'SR_ZCE(白糖期货I)')
    profit2, signal2 = DT(getfuturesdata('data/futures/SR_ZCE'), 20, 0.1, 0.1, 100000, 10, 0.08, 0.5, 1, 'SR_ZCE(白糖期货II)')
    profit3, signal3 = DT(getfuturesdata('data/futures/RB_SHF'), 20, 0.2, 0.2, 100000, 10, 0.08, 0.5, 1, 'RB_SHF(螺纹钢期货I)')
    profit4, signal4 = DT(getfuturesdata('data/futures/RB_SHF'), 20, 0.15, 0.15, 100000, 10, 0.08, 0.5, 1, 'RB_SHF(螺纹钢期货I)')

    profit_address1 = Path('nav_and_result/CTA_SRI' + '_nav.csv')
    signal_address1 = Path('signal/CTA_SRI'+'_signal.csv')
    profit1.to_csv(profit_address1, index=True, header=True)
    signal1.to_csv(signal_address1, index=True, header=True)

    profit_address2 = Path('nav_and_result/CTA_SRII' + '_nav.csv')
    signal_address2 = Path('signal/CTA_SRII' + '_signal.csv')
    profit2.to_csv(profit_address2, index=True, header=True)
    signal2.to_csv(signal_address2, index=True, header=True)

    profit_address3 = Path('nav_and_result/CTA_RBI' + '_nav.csv')
    signal_address3 = Path('signal/CTA_RBI' + '_signal.csv')
    profit3.to_csv(profit_address3, index=True, header=True)
    signal3.to_csv(signal_address3, index=True, header=True)

    profit_address4 = Path('nav_and_result/CTA_RBII' + '_nav.csv')
    signal_address4 = Path('signal/CTA_RBII' + '_signal.csv')
    profit4.to_csv(profit_address4, index=True, header=True)
    signal4.to_csv(signal_address4, index=True, header=True)


if __name__ == "__main__":
    cta()