#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：Genie time:2019/3/19
import numpy
import pandas
import statsmodels.api as sm
import os
from pathlib import Path
import time
# from report_and_figure import ReportAndFigure

# 用多因子框架得到策略position & nav


class MultiFactor(object):
    def __init__(self, bench):

        self.bench = bench

        # 个股数据
        self.close = pandas.read_csv(Path("data/stock/stock_close.csv"),
                                     header=0, index_col=0).sort_index()
        self.high = pandas.read_csv(Path("data/stock/stock_high.csv"),
                                    header=0, index_col=0).sort_index()
        self.low = pandas.read_csv(Path("data/stock/stock_low.csv"),
                                   header=0, index_col=0).sort_index()
        self.industry = self.get_int_date(pandas.read_csv(Path("data/stock/industry.csv"),
                                                          header=0, index_col=0).sort_index())
        self.ipo_date = pandas.read_csv(Path("data/stock/ipo_date.csv"),
                                        header=0, index_col=0).sort_index()
        self.turnover_rate = pandas.read_csv(Path("data/stock/stock_turnover_rate.csv"),
                                             header=0, index_col=0).sort_index()
        self.volume = pandas.read_csv(Path("data/stock/stock_vol.csv"),
                                      header=0, index_col=0).sort_index()
        self.market_value = pandas.read_csv(Path("data/stock/stock_total_mv.csv"),
                                            header=0, index_col=0).sort_index()
        self.market_value = self.market_value.reindex(self.close.index, method="ffill")

        # 指数数据
        self.index_close = self.get_int_date(pandas.read_csv(Path("data/index/index_close.csv"),
                                                             header=0, index_col=0).sort_index())
        self.nday, self.nstock = self.close.shape
        self.index_pct_chg_here = self.get_pct_chg(self.index_close[self.bench])
        self.pct_chg = self.get_pct_chg(self.close)

        self.industry = self.industry.reindex(self.close.index, method="ffill")

    @staticmethod
    def get_int_date(data):

        data.index = [int(each.replace("-", "")) for each in data.index]

        return data

    @staticmethod
    def get_pct_chg(data):

        return (data - data.shift(1)) / data.shift(1)

    @staticmethod
    def get_stack_data(data, name):
        data_new = data.stack().reset_index()
        data_new.columns = ["tradingday", "stock", name]

        return data_new

    def get_ic(self, factor, predict_time):
        # predict_time：计算IC值的周期，即T日的IC值=T日因子值和T+1到T+predict_time期收益率的相关系数
        pct_chg_prod = (1+self.pct_chg).rolling(window=predict_time,
                                                min_periods=int(predict_time / 2)).apply(numpy.prod, raw=True) - 1
        ic = factor.corrwith(pct_chg_prod.shift(-predict_time), axis=1)

        return ic

    def get_ic_mean_df(self, factor, predict_time, num):
        # predict_time：计算IC值的周期，即T日的IC值=T日因子值和T+1到T+predict_time期收益率的相关系数
        # num：用过去多长时间的IC序列计算平均IC值
        ic = self.get_ic(factor, predict_time)
        ic_mean = ic.rolling(window=num, min_periods=int(num / 2)).mean()

        return pandas.DataFrame(numpy.tile(ic_mean.values, [factor.shape[1], 1]).T,
                                index=factor.index, columns=factor.columns)

    def get_ir_df(self, factor, predict_time, num):
        # predict_time：计算IC值的周期，即T日的IC值=T日因子值和T+1到T+predict_time期收益率的相关系数
        # num：用过去多长时间的IC序列计算IR值
        ic = self.get_ic(factor, predict_time)
        ir = ic.rolling(window=num, min_periods=int(num / 2)).mean() / \
             ic.rolling(window=num, min_periods=int(num / 2)).std()

        return pandas.DataFrame(numpy.tile(ir.values, [factor.shape[1], 1]).T,
                                index=factor.index, columns=factor.columns)

    @staticmethod
    def remove_outlier(factor):

        return factor.clip(lower=factor.quantile(.01, interpolation="lower", axis=1),
                           upper=factor.quantile(.99, interpolation="higher", axis=1),
                           axis=0)

    @staticmethod
    def missing_process_industry_mean(factor):

        temp = pandas.DataFrame()
        for pos, data in factor.groupby(["industry", "tradingday"]):
            data["initial_factor"].fillna(data["initial_factor"].mean(), inplace=True)
            temp = pandas.concat([temp, data], axis=0)
        temp = temp.sort_index()

        return temp.loc[:, ["tradingday", "stock", "initial_factor"]].pivot(index="tradingday", columns="stock")

    @staticmethod
    def normalize(factor):

        def normalized_standard(data):
            return (data - data.mean()) / data.std()

        return factor.apply(normalized_standard, axis=1)

    def neutralize(self, factor, mode):
        # mode = 0不中性化；mode = 1;行业中性化；mode = 1;行业和市值中性化
        if mode == 0:
            return factor
        else:
            factor_stack = self.get_stack_data(factor, "factor")
            industry_stack = self.get_stack_data(self.industry, "industry")
            market_value_stack = self.get_stack_data(self.market_value, "market_value")
            df = pandas.concat([factor_stack, industry_stack["industry"], market_value_stack["market_value"]], axis=1)

            temp = pandas.DataFrame()
            for day, data in df.groupby("tradingday"):
                dummy_industry = pandas.get_dummies(data["industry"])
                y = data["factor"]
                if mode == 1:
                    result = sm.OLS(y.astype(float), dummy_industry.astype(float)).fit()
                    neutralized_factor = result.resid
                elif mode == 2:
                    x = pandas.concat([data["market_value"], dummy_industry], axis=1)
                    result = sm.OLS(y.astype(float), x.astype(float)).fit()
                    neutralized_factor = result.resid
                else:
                    print("wrong mode in neutralization")
                    break
                data["neutralized_factor"] = neutralized_factor
                temp = pandas.concat([temp, data], axis=0)

            return temp.loc[:, ["tradingday", "stock", "neutralized_factor"]].pivot(index="tradingday", columns="stock")

    # calculator factor
    def calc_beta_factor(self):

        n1 = 252
        n2 = 126
        std_stock = self.pct_chg.rolling(window=n1, min_periods=int(n1/3)).std()
        # std_bench = self.index_pct_chg_here.rolling(window=n1, min_periods=int(n1/3)).std()
        pho = self.pct_chg.rolling(window=n2, min_periods=int(n2/3)).corr(self.index_pct_chg_here)
        beta_simple = pho * std_stock

        return beta_simple

    def calc_volatility_4(self, window=20):

        high = self.high.fillna(method="pad")
        low = self.low.fillna(method="pad")
        res = (high - low) / low

        return res.rolling(window).std()

    def calc_momentum(self, window=20):

        momentum = self.close / self.close.shift(window) - 1.

        return -momentum

    # dispose factor   mode = 0不中性化；mode = 1;行业中性化；mode = 1;行业和市值中性化
    def dispose_factor(self, initial_factor, mode=0):

        # 1、剔除volume=0的股票; 剔除ST的股票；
        initial_factor[self.volume == 0.] = numpy.nan
        initial_factor[self.volume.isna()] = numpy.nan

        # 2、去极值
        factor2 = self.remove_outlier(initial_factor)

        # # 3、缺失值处理：设为行业内股票因子值的均值
        # factor_stack = self.get_stack_data(factor2, "initial_factor")
        # industry_stack = self.get_stack_data(self.industry, "industry")
        # temp1 = pandas.merge(factor_stack, industry_stack, how="right", on=["tradingday", "stock"])
        # factor3 = pandas.DataFrame(self.missing_process_industry_mean(temp1).values,
        #                            index=factor2.index, columns=factor2.columns)

        # 4、正态标准化
        factor3 = factor2
        factor4 = self.normalize(factor3)

        # 5、行业中性化、市值中性化
        factor5 = self.neutralize(factor4, mode)

        # 6、正态标准化
        factor6 = self.normalize(factor5)

        return factor6

    # combine factor    mode=0:等权(也分正负)；mode=1:按IC加权；mode=2:按IR加权；
    def get_combine_factor(self, *factor, predict_time=2, num=5, mode=0):

        combine_factor = pandas.DataFrame()

        if mode == 0:
            for data in factor:
                ic_mean_df = self.get_ic_mean_df(data, predict_time, num)
                combine_factor = combine_factor.add(data.multiply(numpy.sign(ic_mean_df)), fill_value=.0)

        elif mode == 1:
            for data in factor:
                ic_mean_df = self.get_ic_mean_df(data, predict_time, num)
                combine_factor = combine_factor.add(data.multiply(ic_mean_df), fill_value=.0)

        elif mode == 2:
            for data in factor:
                ir_df = self.get_ir_df(data, predict_time, num)
                combine_factor = combine_factor.add(data.multiply(ir_df), fill_value=.0)

        else:
            print("error weight mode")

        return combine_factor

    # stock selection & compute position T日记录的是下一期的股票权重
    def stock_selection_and_position(self, combine_factor, stock_num=5, mode=0):
        # begin_time: 回测开始时间 前一天就要计算
        # predict_time：换仓周期
        # stock_num：选择的股票数目
        # mode=0: 选出股票后等权持有；mode=1: 选出股票后按因子值加权

        def get_small_factor_stock(data):

            value = stock_num / combine_factor.shape[1]
            return data <= data.quantile(value)

        temp = combine_factor.apply(get_small_factor_stock, axis=1)
        stock_signal = pandas.DataFrame(0, index=temp.index, columns=temp.columns)
        stock_signal[temp] = 1

        def factor_minus_median(data):

            return abs(data - data.quantile(0.5))

        if mode == 0:
            stock_position = stock_signal
        elif mode == 1:
            distance = combine_factor.apply(factor_minus_median, axis=1)
            stock_position = stock_signal * distance
        else:
            print("error position mode")

        stock_position.fillna(0., inplace=True)

        def normalizing(data):
            # 归一
            if data.sum() != 0:
                return data / data.sum()
            else:
                return data

        return stock_position.apply(normalizing, axis=1)

    def get_signal(self, position, predict_time):

        position_here = position.iloc[range(0, len(position), predict_time), :]
        signal = pandas.DataFrame(index=position_here.index, columns=["signal", "trade_date", "trade_code"])
        for pos in position_here.index:

            position_temp = position_here.loc[pos, position_here.loc[pos, :] != .0]
            signal.loc[pos, "signal"] = ','.join(str(i) for i in position_temp.values)
            signal.loc[pos, "trade_code"] = ','.join(str(i) for i in position_temp.index)
            signal.loc[pos, "trade_date"] = pandas.to_datetime(str(pos)).date()

        return signal

    # 输入权重矩阵计算净值
    def backtest(self, position, predict_time=5, begin_time=20100105, cost_coeff=0.003):
        # position: 权重dataframe  T日记录的是下一期的股票权重
        # predict_time：换仓周期
        # begin_time: 回测开始时间
        # cost_coeff：交易成本
        begin_pos = numpy.where(position.index >= begin_time)[0][0]
        exchange_id = numpy.arange(begin_pos - 1, self.nday, predict_time)
        exchange_times = len(exchange_id)  # 换仓次数

        ret_portfolio = numpy.zeros([self.nday])
        for i in range(exchange_times - 1):
            returns_here = self.pct_chg.values[exchange_id[i] + 1:exchange_id[i + 1] + 1, :]  # 持仓阶段每日的returns。
            weight_here = position.iloc[exchange_id[i], :]
            stock_ret = weight_here.values.reshape(1, len(weight_here)) * returns_here
            ret_portfolio[exchange_id[i] + 1:exchange_id[i + 1] + 1] = pandas.DataFrame(stock_ret).sum(axis=1).values

        ret_hedge = ret_portfolio - self.index_pct_chg_here.values
        ret_hedge = ret_hedge[begin_pos:]
        ret_hedge[0] = .0
        nav = pandas.DataFrame()
        nav["net_value"] = numpy.cumprod(1+ret_hedge)
        nav.index = position.index[begin_pos:]
        nav.index = nav.index.astype(str)
        nav.index = ['-'.join([each[0:4], each[4:6], each[6:]]) for each in nav.index]
        nav.index.name = "trade_date"

        return nav


def multi_factor():

    begin_time = 20100104
    cost_coeff = 0.003
    bench = "399300.SZ"

    factor_name_all = ["volatility_4", "momentum"]  # "market_value"
    predict_time_all = [5, 10, 20]
    stock_num_all = [10, 20, 50, 100]
    window_all = [5, 10, 20]

    for factor_name in factor_name_all:
        for predict_time in predict_time_all:
            for stock_num in stock_num_all:
                for window in window_all:

                    print(factor_name, predict_time, predict_time, window)

                    MF = MultiFactor(bench)
                    print("==============calculate factor==============")
                    func = getattr(MF, "calc_%s" % factor_name)
                    initial_factor1 = func(window)
                    # initial_factor1 = MF.market_value

                    print("==============start dispose_factor==============")
                    factor1 = MF.dispose_factor(initial_factor1, mode=0)

                    # print("==============combine factor==============")
                    # combine_factor = temp.get_combine_factor(factor1, factor2, factor3, predict_time=predict_time, num=IC_num, mode=0)
                    # combine_factor.to_csv(os.path.join(dir_here, "combine_factor.csv"), index=True, header=True)
                    combine_factor = factor1

                    print("==============start stock_selection_and_position==============")
                    position = MF.stock_selection_and_position(combine_factor, stock_num, mode=0)

                    print("==============start get_signal==============")
                    signal = MF.get_signal(position, predict_time)
                    signal.to_csv(Path("signal/multi_factor_%s_cycle%d_stock_num%d_window%d_signal.csv" % (factor_name, predict_time, stock_num, window)),
                                  index=True, header=True)

                    print("==============start backtest==============")
                    nav = MF.backtest(position, predict_time, begin_time, cost_coeff)
                    nav.to_csv(Path("nav_and_result/multi_factor_%s_cycle%d_stock_num%d_window%d_nav.csv" % (factor_name, predict_time, stock_num, window)),
                               index=True, header=True)

                    # plot
                    from datetime import datetime
                    nav.index = [datetime.strptime(d, '%Y-%m-%d').date() for d in nav.index]
                    from matplotlib import pyplot as plt
                    plt.plot(nav.index, nav.net_value)
                    plt.savefig("multi_factor_%s_cycle%d_stock_num%d_window%d" % (factor_name, predict_time, stock_num, window)+".png")
                    # figsize = (6, 4)
                    # fig, ax = plt.subplots(figsize=figsize)
                    # ax.plot(nav, 'b', label='nav_portfolio')
                    # ax.legend(loc="best")
                    # plt.title("nav")
                    # plt.xticks(rotation=45)
                    # # plt.savefig(file_name)
                    # plt.show()


if __name__ == "__main__":
    multi_factor()


