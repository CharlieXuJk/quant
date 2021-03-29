from myBaostock import Baostock
from database import Mysql
import backtrader as bt
from datetime import datetime

if __name__ == "__main__":
    bao = Baostock.BaostockRebuild()
    sh000001 = bao.k_data_query(code="000001.SH", char="date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg",
                 start_date="2019-03-10", end_date="2020-01-01", frequency="d", adjustflag="3")
    #sh000001.to_csv("Test.csv")

    #div_info_test = bao.div_info_query(code="sh.600000", year="2015", yearType="report")

    #profitability_info = bao.profitability_info_query(code="sh.600000", year=2017, quarter=2)
    #print(profitability_info)

    db = Mysql.MysqlConnector(host="1.15.90.134", user="gtrepublic", passwd="123", auth_plugin="mysql_native_password")
    #db.createTable("sh000001")
    #db.uploadData(sh000001, "sh000001")
    pdd = db.downloadData("sh000001")
    print(pdd.head())


    # 创建策略类
    class SmaCross(bt.Strategy):
        # 定义参数
        params = dict(period=5  # 移动平均期数
                      )

        # 日志函数
        def log(self, txt, dt=None):
            '''日志函数'''
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

        def notify_order(self, order):
            if order.status in [order.Submitted, order.Accepted]:
                # 订单状态 submitted/accepted，无动作
                return

            # 订单完成
            if order.status in [order.Completed]:
                if order.isbuy():
                    self.log('买单执行, %.2f' % order.executed.price)

                elif order.issell():
                    self.log('卖单执行, %.2f' % order.executed.price)

            elif order.status in [order.Canceled, order.Margin, order.Rejected]:
                self.log('订单 Canceled/Margin/Rejected')

        # 记录交易收益情况（可省略，默认不输出结果）
        def notify_trade(self, trade):
            if trade.isclosed:
                print('毛收益 %0.2f, 扣佣后收益 % 0.2f, 佣金 %.2f' %
                      (trade.pnl, trade.pnlcomm, trade.commission))

        def __init__(self):
            # 移动平均线指标
            self.move_average = bt.ind.MovingAverageSimple(
                self.data, period=self.params.period)

            # 交叉信号指标
            self.crossover = bt.ind.CrossOver(self.data, self.move_average)

        def next(self):

            if not self.position:  # 还没有仓位
                # 当日收盘价上穿5日均线，创建买单，买入100股
                if self.crossover > 0:
                    self.log('创建买单')
                    self.buy(size=100)
            # 有仓位，并且当日收盘价下破5日均线，创建卖单，卖出100股
            elif self.crossover < 0:
                self.log('创建卖单')
                self.sell(size=100)


    ##########################
    # 主程序开始
    #########################

    # 创建大脑引擎对象
    cerebro = bt.Cerebro()

    data = bt.feeds.PandasData(
        dataname=pdd,
        datetime='date',  # 日期列
        open=2,  # 开盘价所在列
        high=3,  # 最高价所在列
        low=4,  # 最低价所在列
        close=5,  # 收盘价价所在列
        volume=7,  # 成交量所在列
        openinterest=-1,  # 无未平仓量列.(openinterest是期货交易使用的)
        fromdate=datetime(2019, 5, 1),  # 起始日
        todate=datetime(2020, 7, 8)  # 结束日
    )

    cerebro.adddata(data)  # 将行情数据对象注入引擎
    cerebro.addstrategy(SmaCross)  # 将策略注入引擎

    cerebro.broker.setcash(10000000.0)  # 设置初始资金
    cerebro.broker.setcommission(0.001)  # 佣金费率
    # 固定滑点，也可用cerebro.broker.set_slippage_perc()设置百分比滑点
    cerebro.broker.set_slippage_fixed(0.05)

    print('初始市值: %.2f' % cerebro.broker.getvalue())
    cerebro.run()  # 运行
    print('最终市值: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()