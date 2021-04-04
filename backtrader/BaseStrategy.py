import Baostock as bs
import pandas as pd

# 创建策略类
class SmaCross(bt.Strategy):
    # 日志函数
    def log(self, txt, dt=None):
        '''日志函数'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        self.log('订单状态 %s' %order.getstatusname())
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

    def myBuy(self, size=100):
        self.log('创建买单')
        validday = self.data.datetime.datetime(1)
        print('validay', validday)
        uppertradinglimit = self.data.close[0] * 1.1 -0.02
        self.order = self.buy(
            size=size,
            valid=validday,
            exectype=bt.Order.Limit,
            price=uppertradinglimit
        )

    def myBuy(self, size=100):
        self.log('创建买单')
        validday = self.data.datetime.datetime(1)
        print('validay', validday)
        uppertradinglimit = self.data.close[0] * 1.1 -0.02
        self.order = self.buy(
            size=size,
            valid=validday,
            exectype=bt.Order.Limit,
            price=uppertradinglimit
        )