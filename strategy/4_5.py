class MyStrategy(bt.Strategy):
    def __init__(self):
        macd_week = bt.ind.MACD(self.data[1], period_mel=12,period_me2=26,period_signal=9)
        macd_day = bt.ind.MACD(self.data, period_me1=12,period_me2=26,period_signal=9)

        self.macd_week = macd_week.macd
        self.signal_week = macd_week.signal
        self.histo_week = self.macd_week - self.signal_week

        self.macd_day = macd_day.macd
        self.signal_day = macd_day.signal
        self.histo_day = self.macd_day - self.signal_day
        #周线金叉
        crossover_macd_week = bt.ind.CrossOver(self)
        sma1 = btind.SimpleMovingAverage(self.data)
        ema1 = btind.ExponentialMovingAverage()
        close_over_sma = self.data.close > sma1
        close_over_ema = self.data.close > ema1
        sma_ema_diff = sma - ema
        buy_sig = bt.And(close_over_sma, close_over_ema, sma_ema_diff > 0)



    def next(self):
        if buy_sig:
            self.buy()
