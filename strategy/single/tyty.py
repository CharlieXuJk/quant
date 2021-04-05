

class MyStrategy(bt.Strategy):
    def __init__(self):
        sma1 = btind.SimpleMovingAverage(self.data)
        ema1 = btind.ExponentialMovingAverage()
        close_over_sma = self.data.close > sma1
        close_over_ema = self.data.close > ema1
        sma_ema_diff = sma - ema
        buy_sig = bt.And(close_over_sma, close_over_ema, sma_ema_diff > 0)



    def next(self):
        if buy_sig:
            self.buy()
