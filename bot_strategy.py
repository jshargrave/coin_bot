import bot_data as bd
import bot_trade as bt
import graph_data as gd
from datetime import *
import config as cfg


class BotStrategy():
    def __int__(self):
        self._buy_vote = 0
        self._sell_vote = 0


    # This function is used to monitor and detect whenever significant changes have occured.  All strategies are
    # called from this function when a significant price has been detected.
    def monitor_price(self, data_look_back=cfg.MONITOR_DR, refresh=cfg.MONITOR_R, look_ahead_per=cfg.MONITOR_LA_PER):
        begin_date = bd.BotData().parse_time(str(datetime.utcnow() - timedelta(seconds=data_look_back)))
        date_range = (begin_date, bd.BotData().parse_time(str(datetime.utcnow())))
        newest_max = -1, -1
        newest_min = -1, -1
        y = []
        x = []

        interval_time = datetime.utcnow().replace(second=0, microsecond=0)
        while True:
            # variable used to hold the current time
            now_time = datetime.utcnow().replace(second=0, microsecond=0)

            # checking if interval has completed
            if interval_time == now_time:
                select = bd.BotData().select_bitcoin_real_time(date_range)

                for row in select:
                    values = (bd.BotData().parse_time(row[1]), float(row[2]))
                    y.append(values[1])
                    x.append(values[0])

                n = len(y)
                if n > 0:
                    mean = sum(y) / n
                    std = bd.BotData().std(bd.BotData().var(mean, y))
                    price = y[-1]

                    # Processing Data
                    local_maximums = bd.BotData().calculate_local_max(x, y, int(n * look_ahead_per) + 1, std)
                    local_minimums = bd.BotData().calculate_local_min(x, y, int(n * look_ahead_per) + 1, std)
                    absolute_max = bd.BotData().find_absolute_max(x, y)
                    absolute_min = bd.BotData().find_absolute_min(x, y)

                    # Graphing data
                    gd.GraphChart().graph_data(x, y, local_maximums, local_minimums, absolute_max, absolute_min)

                    if newest_max == (-1, -1) and newest_min == (-1, -1):
                        newest_max = local_maximums[-1]
                        newest_min = local_minimums[-1]

                    # Checking for significant changes, and then running strategies
                    if newest_max != local_maximums[-1] or self.is_price_stable(x, y):
                        newest_max = local_maximums[-1]
                        print("Found new local max, running strategies...")
                        self.potential_gain_strategy(absolute_max, price, "buy")

                    if newest_min != local_minimums[-1] or self.is_price_stable(x, y):
                        newest_min = local_minimums[-1]
                        print("Found new local min, running strategies...")
                        self.potential_gain_strategy(absolute_max, price, "sell")

            # updating interval_time
            if interval_time <= now_time:
                interval_time = now_time + timedelta(minutes=refresh)
                date_range = (date_range[1], interval_time)


    # Running average works by computing the running average of a set amount of historical time.  If the average is
    # increasing, we invest.  If the average is decreasing, we sell.
    def running_avg_strategy(self):
        pass

    # The stability approach works by investing only during stable prices.  This is a more long term approach, that
    # assumes prices will stagnate, and then become noising again.
    def is_price_stable(self, x, y, data_look_back=cfg.STABLE_DR, threshold=cfg.STABLE_T):
        begin_date = bd.BotData().parse_time(str(datetime.utcnow() - timedelta(seconds=data_look_back)))
        date_range = (begin_date, bd.BotData().parse_time(str(datetime.utcnow())))

        x_stable = []
        y_stable = []

        # removing elements outside of date range
        for x_obj, y_obj in zip(x, y):
            if x_obj > date_range[0] or x_obj < date_range[1]:
                x_stable.append(x_obj)
                y_stable.append(y_obj)

        n = len(y)
        if n > 0:
            mean = sum(y) / n
            std = bd.BotData().std(bd.BotData().var(mean, y))
            in_std_count = 0.0

            for item in y_stable:
                if item < mean + std and item > mean - std:
                    in_std_count += 1

            stability_prob = in_std_count / n
            print "Stability is %.4f." % stability_prob
            if stability_prob > threshold:
                print "Probability of stable price is %.4f." % stability_prob
                return True


    # The potential gain approach works by using the absolute max/min as a proof of concept.  Comparing the current
    # price with what is can be in the future.
    def potential_gain_strategy(self, absolute_max, price, method, gain_per=cfg.POTENTIAL_GP):
        if method == "buy":
            price_gain_per = (absolute_max[1] - price) / absolute_max[1]

            # if current potential gain > gain percent set
            if price_gain_per > gain_per:
                print "Buying at %.4f gain." % price_gain_per

        elif method == "sell":
            pass

    # The linear regression strategy works by computing two linear regressions, one over a longer peroid of data, and
    # one over a shorter period of data.  We can then compare the two, and based on the diffrences we can decide to buy
    # or sell.
    def linear_regression_strategy(self):
        pass