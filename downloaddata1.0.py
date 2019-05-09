import tushare as ts
import pandas as pd
import time
import os
import pickle
from datetime import datetime, date, timedelta
from pathlib import Path



#下载以及更新指数数据
def getindexquota(symbols,start_date,end_date):
    factors_quota = ['open','close','high','low','vol','amount']
    panel  = {factors_quota[0]: pd.DataFrame(),
              factors_quota[1]: pd.DataFrame(),
              factors_quota[2]: pd.DataFrame(),
              factors_quota[3]: pd.DataFrame(),
              factors_quota[4]: pd.DataFrame(),
              factors_quota[5]: pd.DataFrame(),
             }
    for i in symbols:
        index  = pro.index_daily(ts_code=i, start_date = start_date, end_date = end_date)
        for j in factors_quota:
            panel[j]['trade_date'] = index['trade_date']
            panel[j][i] = index[j]
    for i in factors_quota:
        panel[i]['trade_date'] =pd.to_datetime(panel[i]['trade_date'])
        panel[i] = panel[i].set_index('trade_date')
        panel[i].to_csv(Path('data/index/index_' + i +'.csv'))

def updateindexquota():
    factors_quota = ['open','close','high','low','vol','amount']
    panel  = {factors_quota[0]: pd.DataFrame(),
              factors_quota[1]: pd.DataFrame(),
              factors_quota[2]: pd.DataFrame(),
              factors_quota[3]: pd.DataFrame(),
              factors_quota[4]: pd.DataFrame(),
              factors_quota[5]: pd.DataFrame(),
             }
    old_data = pd.read_csv(Path('data/index/index_close.csv'),index_col = 0,dtype = {'trade_date':str})
    start_date = (old_data.index)[0]
    strat_date = datetime.strptime(str(start_date), '%Y-%m-%d').date()

    tommorow = (strat_date + timedelta(days = 1)).strftime('%Y%m%d')
    end_date = time.strftime('%Y%m%d', time.localtime(time.time()))
    if  strat_date.strftime('%Y%m%d') == end_date:
        return True
    for i in old_data.columns:
        index  = pro.index_daily(ts_code=i, start_date = tommorow, end_date = end_date)
        for j in factors_quota:
            panel[j]['trade_date'] = index['trade_date']
            panel[j][i] = index[j]
    try:
        for i in factors_quota:
            panel[i]['trade_date'] =pd.to_datetime(panel[i]['trade_date'])
            panel[i] = panel[i].set_index('trade_date')
            old_data = pd.read_csv(Path('data/index/index_' + i + '.csv'),index_col = 0,dtype = {'trade_date':str})
            old_data.index = pd.to_datetime(old_data.index)
            new_data  = pd.concat([panel[i],old_data],axis = 0)
            new_data.to_csv(Path('data/index/index_' + i +'.csv'))
        return True
    except:
        return False

#下载以及更新股票数据
def getstockquota(symbols, start_date, end_date):
    factors_quota = ['open', 'close', 'high', 'low', 'vol', 'amount']
    panel = {factors_quota[0]: pd.DataFrame(),
             factors_quota[1]: pd.DataFrame(),
             factors_quota[2]: pd.DataFrame(),
             factors_quota[3]: pd.DataFrame(),
             factors_quota[4]: pd.DataFrame(),
             factors_quota[5]: pd.DataFrame(),
             }
    k = 0
    for i in symbols:
        try:
            stock = ts.pro_bar(pro_api=pro, ts_code=i, adj='hfq', start_date=start_date, end_date=end_date)
            for j in factors_quota:
                panel[j]['trade_date'] = stock['trade_date']
                panel[j][i] = stock[j]
                panel[j].to_pickle(str('stock_' + j + '.pkl'))
            print
            k
            k = k + 1
        except:
            time.sleep(10)
            stock = ts.pro_bar(pro_api=pro, ts_code=i, adj='hfq', start_date=start_date, end_date=end_date)
            for j in factors_quota:
                panel[j]['trade_date'] = stock['trade_date']
                panel[j][i] = stock[j]
                panel[j].to_pickle(str('stock_' + j + '.pkl'))
            print
            k
            k = k + 1
    for i in factors_quota:
        panel[i]['trade_date'] = pd.to_datetime(panel[i]['trade_date'])
        panel[i] = panel[i].set_index('trade_date')
        panel[i].to_csv(Path('data/stock/stock_' + i + '.csv'))

def updatestockquota():
    factors_quota = ['open', 'close', 'high', 'low', 'vol', 'amount']
    panel = {factors_quota[0]: pd.DataFrame(),
             factors_quota[1]: pd.DataFrame(),
             factors_quota[2]: pd.DataFrame(),
             factors_quota[3]: pd.DataFrame(),
             factors_quota[4]: pd.DataFrame(),
             factors_quota[5]: pd.DataFrame(),
             }
    old_data = pd.read_csv(Path('data/stock/stock_close.csv'), index_col=0, dtype={'trade_date': str})
    start_date = (old_data.index)[-1]
    strat_date = datetime.strptime(str(start_date), '%Y%m%d').date()
    tommorow = (strat_date + timedelta(days=1)).strftime('%Y%m%d')
    end_date = time.strftime('%Y%m%d', time.localtime(time.time()))
    if  strat_date.strftime('%Y%m%d') == end_date:
        return True
    k = 0
    for i in old_data.columns:
        try:
            stock = ts.pro_bar( ts_code=i, adj='hfq', start_date=tommorow, end_date=end_date)
            for j in factors_quota:
                panel[j]['trade_date'] = stock['trade_date']
                panel[j][i] = stock[j]
                #panel[j].to_pickle(str('stock_' + j + '.pkl'))
            print (k)
            k = k + 1
        except:
            time.sleep(10)
            stock = ts.pro_bar( ts_code=i, adj='hfq', start_date=tommorow, end_date=end_date)
            for j in factors_quota:
                panel[j]['trade_date'] = stock['trade_date']
                panel[j][i] = stock[j]
                #panel[j].to_pickle(str('stock_' + j + '.pkl'))
            print (k)
            k = k + 1
    try:
        for i in factors_quota:
            panel[i] = panel[i].set_index('trade_date')
            panel[i] = panel[i].sort_index()
            old_data = pd.read_csv(Path('data/stock/stock_' + i + '.csv'), index_col=0, dtype={'trade_date': str})
            new_data = pd.concat([old_data, panel[i]], axis=0)
            new_data.to_csv(Path('data/stock/stock_' + i + '.csv'))
        return True
    except:
        return False

def getstockbasic(symbols, start_date, end_date):
    factors_basic = ['turnover_rate', 'pe', 'pb', 'total_share', 'total_mv']
    panel = {factors_basic[0]: pd.DataFrame(),
             factors_basic[1]: pd.DataFrame(),
             factors_basic[2]: pd.DataFrame(),
             factors_basic[3]: pd.DataFrame(),
             factors_basic[4]: pd.DataFrame(),
             }
    k = 0
    for i in symbols:
        try:
            stock_basic = pro.daily_basic(ts_code=i, start_date=tommorow, end_date=end_date,
                                          fields='trade_date,turnover_rate,pe,pb,total_share,total_mv')
            for j in factors_basic:
                panel[j]['trade_date'] = stock_basic['trade_date']
                panel[j][i] = stock_basic[j]
                panel[j].to_pickle(str('stock_' + j + '.pkl'))
            print
            k
            k = k + 1
        except:
            time.sleep(10)
            stock_basic = pro.daily_basic(ts_code=i, start_date=tommorow, end_date=end_date,
                                          fields='trade_date,turnover_rate,pe,pb,total_share,total_mv')

            for j in factors_basic:
                panel[j]['trade_date'] = stock_basic['trade_date']
                panel[j][i] = stock_basic[j]
                panel[j].to_pickle(str('stock_' + j + '.pkl'))
            print
            k
            k = k + 1

    for i in factors_basic:
        panel[i] = panel[i].set_index('trade_date')
        panel[i].to_csv(Path('data/stock/stock_' + i + '.csv'))

def updatestockbasic():
    factors_basic = ['turnover_rate', 'pe', 'pb', 'total_share', 'total_mv']
    panel = {factors_basic[0]: pd.DataFrame(),
             factors_basic[1]: pd.DataFrame(),
             factors_basic[2]: pd.DataFrame(),
             factors_basic[3]: pd.DataFrame(),
             factors_basic[4]: pd.DataFrame(),
             }
    k = 0
    old_data = pd.read_csv(Path('data/stock/stock_pe.csv'), index_col=0, dtype={'trade_date': str})
    start_date = (old_data.index)[0]
    strat_date = datetime.strptime(str(start_date), '%Y%m%d').date()
    tommorow = (strat_date + timedelta(days=1)).strftime('%Y%m%d')
    end_date = time.strftime('%Y%m%d', time.localtime(time.time()))
    if  strat_date.strftime('%Y%m%d') == end_date:
        return True
    for i in old_data.columns:
        try:
            stock_basic = pro.daily_basic(ts_code=i, start_date=tommorow, end_date=end_date,
                                          fields='trade_date,turnover_rate,pe,pb,total_share,total_mv')
            for j in factors_basic:
                panel[j]['trade_date'] = stock_basic['trade_date']
                panel[j][i] = stock_basic[j]
                #panel[j].to_pickle(str('stock_' + j + '.pkl'))
            print (k)
            k = k + 1
        except:
            time.sleep(10)
            stock_basic = pro.daily_basic(ts_code=i, start_date=tommorow, end_date=end_date,
                                          fields='trade_date,turnover_rate,pe,pb,total_share,total_mv')

            for j in factors_basic:
                panel[j]['trade_date'] = stock_basic['trade_date']
                panel[j][i] = stock_basic[j]
                #panel[j].to_pickle(str('stock_' + j + '.pkl'))
            print (k)
            k = k + 1
    try:
        for i in factors_basic:
            panel[i] = panel[i].set_index('trade_date')
            old_data = pd.read_csv(Path('data/stock/stock_' + i + '.csv'), index_col=0, dtype={'trade_date': str})
            new_data = pd.concat([panel[i], old_data], axis=0)
            new_data.to_csv(Path('data/stock/stock_' + i + '.csv'))
        return True
    except:
        return False

#下载以及更新期货数据
def downloadfuturesquota(symbols,start_date,end_date):
    for i in symbols:
        try:
            temp = pro.fut_daily(ts_code=i, start_date=start_date, end_date=end_date,fields = 'ts_code,trade_date,open,high,low,close,amount,vol,oi')
            temp = temp.sort_values(by = 'trade_date',ascending=True)
            temp.index = [j for j in range(len(temp.index))]
            temp['trade_date'] = temp['trade_date'].values
            address =  'data/futures/' + i.replace('.','_') + '.csv'
            temp.to_csv(address)
            return True
        except:
            return False

def updatefuturesquota(filename):
    try:
        old_data = pd.read_csv(filename,index_col = 0,dtype = {'ts_code':str, 'trade_date':str})
        start_date = (old_data['trade_date'].values)[-1]
        strat_date = datetime.strptime(str(start_date), '%Y%m%d').date()
        tommarow = (strat_date + timedelta(days = 1)).strftime('%Y%m%d')
        end_date = time.strftime('[%Y%m%d]', time.localtime(time.time()))
        if strat_date.strftime('%Y%m%d') == end_date:
            return True
        temp = pro.fut_daily(ts_code=(old_data['ts_code'].values)[-1], start_date=tommarow, end_date=end_date,fields = 'ts_code,trade_date,open,high,low,close,amount,vol,oi')
        temp = temp.sort_values(by = 'trade_date',ascending=True)
        new_data  = pd.concat([old_data,temp],axis = 0)
        new_data.index = [j for j in range(len(new_data.index))]
        new_data.to_csv(filename)
        return True
    except:
        return False

def updateallfutures():
    ts_code = ['CF.ZCE','SR.ZCE','RB.SHF','RU.SHF','IF.CFX']
    for i in ts_code:
        try:
            address = 'data/futures/' + i.replace('.','_')+'.csv'
            updatefuturesquota(address)
        except:
            print (i)
            return False
    return True

def updatedatabase():
    ts.set_token('fd26fb147d36e7990dc877794c55ee2cde8db22c91559df61516600e')
    pro = ts.pro_api()
    index_list = ['000001.SH', '000016.SH', '399300.SZ', '000905.SH', '000012.SH']
    if (updateindexquota()):
        print ('index data updated')
    if (updatestockquota()):
        print('stock quota data updated')
    if (updatestockbasic()):
        print('stock basic data updated')
    if (updateallfutures()):
        print('futures data updated')


# if __name__ == '__main__':
#     ts.set_token('fd26fb147d36e7990dc877794c55ee2cde8db22c91559df61516600e')
#     pro = ts.pro_api()
#     #if (updatestockquota()):
#     #    print('stock quota data updated')
#     if (updatestockbasic()):
#         print ('stock basic data updated')

