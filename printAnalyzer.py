from datetime import datetime
import backtrader as bt
import os.path
import sys

def pretty_print(format, *args):
    print(format.format(*args))

def exists(object, *properties):
    for property in properties:
        if not property in properties:
            return False
        object = object.get(property)
        return True

def printTradeAnalysis(cerebro, analyzers):
    format = " {:<24} : {:<24}"
    NA      = '-'

    print('Backtesting Results')
    if hasattr(analyzers, 'ta'):
        ta = analyzers.ta.get_analysis()

        openTotal = ta.total.open if exists(ta, 'total', 'open') else None
        closedTotal = ta.total.closed if exists(ta, 'total', 'closed') else None
        wonTotal = ta.won.total if exists(ta, 'won', 'total') else None
        lostTotal = ta.lost.total if exists(ta, 'lost', 'total') else None

        streakWonLongest = ta.streak.won.longest if exists(ta, 'streak', 'won', 'longest') else None
        streakLostLongest = ta.streak.lost.longest if exists(ta, 'streak', 'lost', 'longest') else None

        pnlNetTotal = ta.pnl.net.total if exists(ta, 'pnl', 'net', 'total') else None
        pnlNetAverage = ta.pnl.net.average if exists(ta, 'pnl', 'net', 'average') else None

        pretty_print(format, 'Open Postitions', openTotal or NA)
        pretty_print(format, 'Closed Trades', closedTotal or NA)
        pretty_print(format, 'Winning Trades', wonTotal or NA)
        pretty_print(format, 'Losing Trades', lostTotal or NA)
        print('\n')

        pretty_print(format, 'Longest Winning Streak', streakWonLongest or NA)
        pretty_print(format, 'Longest Losing Streak', streakLostLongest or NA)