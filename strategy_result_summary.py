#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：Genie time:2019/4/13

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：Genie time:2019/3/22
import numpy
import pandas
import math
import os
from pathlib import Path
from matplotlib import pyplot as plt
from datetime import datetime


# 每个策略绩效分析保存到一个csv
class ReportAndFigure(object):
    def __init__(self, bench, out_dir):

        self.annual_day = 245
        self.riskfree_rate = 0.
        self.out_path = out_dir
        self.bench = bench

        # 指数数据
        self.index_close = self.get_int_date(pandas.read_csv(Path("data/index/index_close.csv"),
                                                             header=0, index_col=0).sort_index())
        self.index_pct_chg_here = self.get_pct_chg(self.index_close[self.bench])

    @staticmethod
    def get_int_date(data):
        data.index = [int(each.replace("-", "")) for each in data.index]

        return data

    @staticmethod
    def get_pct_chg(data):

        return (data - data.shift(1)) / data.shift(1)

    def calc_annual_return(self, data):

        day_here = len(data)
        ret = data.ret

        return math.pow((1 + ret).prod(), self.annual_day/day_here) - 1

    def calc_sharpe_ratio(self, data):

        return (data.ret.mean()-self.riskfree_rate) / data.ret.std() * numpy.sqrt(self.annual_day)

    @staticmethod
    def calc_maximum_drawdown(data):

        nav = (1+data.ret).cumprod()

        return max((nav.cummax() - nav) / nav.cummax())

    def calc_turnover(self, data):

        temp = 0
        turnover = []
        for date, data_day in data.groupby("date"):
            data_day = data_day.set_index("stock")
            if temp == 0:
                position_today = data_day.position
                turnover.append(position_today.abs().sum() / 2)
                position_yesterday = position_today
                temp = 1

            else:
                position_today = data_day.position
                turnover.append(position_today.sub(position_yesterday, fill_value=0.0).abs().sum() / 2)
                position_yesterday = position_today

        return numpy.mean(turnover) * self.annual_day

    def result(self, nav_portfolio, strategy_name):
        # nav_portfolio: 行是日期，仅记录策略nav的dataframe

        # 收益率
        ret = pandas.DataFrame(index=nav_portfolio.index)
        ret["ret"] = nav_portfolio / nav_portfolio.shift() - 1
        ret.iloc[0] = nav_portfolio.iloc[0] - 1

        # 每年的绩效分析
        result = pandas.DataFrame(index=[strategy_name],
                                  columns=["annual_ret", "sharpe_ratio", "maximum_drawdown"])
        result.loc[strategy_name, "annual_ret"] = self.calc_annual_return(ret)
        result.loc[strategy_name, "sharpe_ratio"] = self.calc_sharpe_ratio(ret)
        result.loc[strategy_name, "maximum_drawdown"] = self.calc_maximum_drawdown(ret)

        return result

    def result_summary(self):

        temp = pandas.DataFrame(columns=["annual_ret", "sharpe_ratio", "maximum_drawdown"])
        for item in os.listdir(self.out_path):
            print(item)
            if item.endswith("_nav.csv"):
                strategy_name = item[:-8]
                nav_portfolio = pandas.read_csv(os.path.join(self.out_path, item), index_col=0, header=0)
                temp = temp.append(self.result(nav_portfolio.net_value, strategy_name))

        # temp.to_csv(os.path.join(self.out_path, "strategy_result_summary.csv"), index=True, header=True)
        temp.to_csv(Path(self.out_path, "strategy_result_summary.csv"), index=True, header=True)

    def get_figure_nav(self):

        for item in os.listdir(self.out_path):
            print(item)
            if item.endswith("_nav.csv"):
                strategy_name = item[:-8]
                nav_portfolio = pandas.read_csv(os.path.join(self.out_path, item), index_col=0, header=0)
                nav_portfolio.index = [datetime.strptime(d, '%Y-%m-%d').date() for d in nav_portfolio.index]

                nav_bench = numpy.cumprod(1+self.index_pct_chg_here)
                nav_bench.index = [datetime.strptime(str(d), '%Y%m%d').date() for d in nav_bench.index]
                nav_portfolio["net_value_bench"] = nav_bench

                figsize = (6, 4)
                fig, ax = plt.subplots(figsize=figsize)
                ax.plot(nav_portfolio.index, nav_portfolio.net_value, 'b', label='nav_portfolio')
                ax.plot(nav_portfolio.index, nav_portfolio.net_value_bench, 'r', label='nav_bench')
                ax.legend(loc="best")
                plt.title("nav")
                plt.xticks(rotation=45)

                file_name = Path(self.out_path, strategy_name+".png")
                plt.savefig(file_name)
                # plt.show()


def main():

    # in_dir = "D:/pycharm/code/robo-advisor/data"
    # out_dir = "D:/pycharm/code/robo-advisor/nav_and_result"  # 不同的电脑上需要设置

    out_dir = "nav_and_result"  # 不同的电脑上需要设置
    bench = "000905.SH"
    temp = ReportAndFigure(bench,  out_dir)
    temp.result_summary()
    # temp.get_figure_nav()


if __name__ == "__main__":
    main()
