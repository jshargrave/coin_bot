import bot_data as bd
import bot_analysis as ba
from datetime import *
import config as cfg
import numpy as np


class BotStrategy:
    def __init__(self):
        self._buy_vote = 0
        self._sell_vote = 0

    '''
    Des: This function is used to monitor and detect whenever significant changes have occurred.  All strategies are
         called from this function when a significant price change has been detected. Variable data_lookback holds a
         int value in sec that determines how much historical data to use.
    Pre: 
    Post:
    '''

    # cfg.BEGIN_DATE_DECREMENT_SEC
    def monitor_price(self):
        end_date = datetime.utcnow().replace(microsecond=0)
        begin_date = end_date - timedelta(seconds=cfg.BEGIN_DATE_DECREMENT_SEC)
        date_range = (begin_date, end_date)

        x = []
        y = []
        local_max_index = []
        local_min_index = []
        append_x = x.append
        append_y = y.append

        select_historical = bd.BotData().select_bitcoin_historical(date_range)
        for row in select_historical:
            append_x(row[1])
            append_y(row[2])

        n = len(y)
        summation_y = sum(y)
        mean = summation_y/n
        var = ba.BotAnalysis().var(mean, y)
        s = ba.BotAnalysis().std(var)

        values = ba.BotAnalysis().find_poi(x, y, mean, s)




    def price_logic(self, x, y, newest_point, index, absolute_max, price, method):
        if self.is_price_stable(x, y, newest_point, index):
            self.potential_gain_strategy(absolute_max, price, method)

    # Running average works by computing the running average of a set amount of historical time.  If the average is
    # increasing, we invest.  If the average is decreasing, we sell.
    def running_avg_strategy(self):
        pass

    # The stability approach works by investing only during stable prices.  This is a more long term approach, that
    # assumes prices will stagnate, and then become noising again.
    def is_price_stable(self, x, y, newest_point, index, data_lookahead=cfg.STABLE_LA, threshold=cfg.STABLE_T):
        pass


    # The potential gain approach works by using the absolute max/min as a proof of concept.  Comparing the current
    # price with what is can be in the future.
    def potential_gain_strategy(self, absolute_max, price, method, gain_per=cfg.POTENTIAL_GP):
        pass


    # The linear regression strategy works by computing two linear regressions, one over a longer peroid of data, and
    # one over a shorter period of data.  We can then compare the two, and based on the diffrences we can decide to buy
    # or sell.
    def linear_regression_strategy(self):
        pass