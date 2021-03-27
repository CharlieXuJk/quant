from datetime import datetime
import backtrader as bt
import os.path  # 管理路径
import sys  # 发现脚本名字(in argv[0])


# %%

import json

with open("stock_pool.json", 'r', encoding='UTF-8') as load_f:
    index = json.load(load_f)

# %%

stock_index = index['股票'].values()
stock_key = index['股票'].keys()


# %%

def tushareToBaostock(str):
    return str.split('.')[1].lower() + '.' + str.split('.')[0]


# %%

temp = "ww.com"
print(tushareToBaostock(temp))

# %%

baostock_index = list(map(tushareToBaostock, stock_index))
c = dict(zip(stock_key, stock_index))

# %%

import pandas as pd
import Baostock as bs

code = list(c.values())[0]
lg = bs.login()
rs = bs.query_history_k_data_plus(code,
                                  "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
                                  start_date='2012-06-01', end_date='2021-3-16',
                                  frequency="d", adjustflag="1")  # frequency="d"取日k线，adjustflag="3"默认不复权
print('query_history_k_data_plus respond error_code:' + rs.error_code)
print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)
data2 = rs.get_data()
data2 = data2.apply(pd.to_numeric, axis=0, errors='ignore')
data2 = data2[data2.tradestatus == 1]
data2['date'] = pd.to_datetime(data2['date'])
print(data2.head())
# %%

print(rs)


def baostockToDataframe(rs):
    li = []
    while (rs.error_code == '0') & rs.next():
        li.append(rs.get_row_data())
    print(li)

    result = pd.DataFrame(li, columns=rs.fields)
    result.close = result.close.astype('float64')
    result.open = result.close.astype('float64')
    result.low = result.low.astype('float64')
    result.high = result.high.astype('float64')
    result.volume = result.volume.astype('int')  # astype转换数组类型
    result = result[result.tradestatus==1]
    result['date'] = pd.to_datetime(result['data'])
   # result.index = pd.to_datetime(result.date)

    return result


# %%

import mysql.connector

# %%

#data = baostockToDataframe(rs.get_data())
# data.to_sql(code, mydb, index=False, if_exists='append')
#print(data.head())

# %%

# 创建策略类
class SmaCross(bt.Strategy):
    # 定义参数
    params = dict(period=5  # 移动平均期数
                  )

    def __init__(self):
        # 移动平均线指标
        self.move_average = bt.ind.MovingAverageSimple(
            self.datas[0].close, period=self.params.period)

    def next(self):

        if not self.position.size:  # 还没有仓位
            # 当日收盘价上穿5日均线，创建买单，买入100股
            if self.datas[0].close[-1] < self.move_average.sma[
                -1] and self.datas[0].close[0] > self.move_average.sma[0]:
                self.buy(size=100)
        # 有仓位，并且当日收盘价下破5日均线，创建卖单，卖出100股
        elif self.datas[0].close[-1] > self.move_average.sma[-1] and self.datas[
            0].close[0] < self.move_average.sma[0]:
            self.sell(size=100)


##########################
# 主程序开始
#########################

# 创建大脑引擎对象
cerebro = bt.Cerebro()

# 获取本脚本文件所在路径
modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
# 拼接得到数据文件全路径
#datapath = os.path.join(modpath, './600000qfq.csv')

# 创建行情数据对象，加载数据
data = bt.feeds.PandasData(
    dataname=data2,
    datetime='date',  # 日期行所在列
    open=2,  # 开盘价所在列
    high=3,  # 最高价所在列
    low=4,  # 最低价所在列
    close=5,  # 收盘价价所在列
    volume=8,  # 成交量所在列
    openinterest=-1,  # 无未平仓量列.(openinterest是期货交易使用的)
    #dtformat=('%Y%m%d'),  # 日期格式
    fromdate=datetime(2019, 1, 1),  # 起始日
    todate=datetime(2020, 7, 8))  # 结束日

cerebro.adddata(data)  # 将行情数据对象注入引擎
cerebro.addstrategy(SmaCross)  # 将策略注入引擎
cerebro.broker.setcash(10000.0)  # 设置初始资金
cerebro.run()  # 运行

print('最终市值: %.2f' % cerebro.broker.getvalue())

cerebro.plot(style='bar')