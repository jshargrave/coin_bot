import bot_data as bd
import bot_trade as bt
import graph_data as gd
from datetime import *
import config as cfg


class BotStrategy:
    def __init__(self):
        self._buy_vote = 0
        self._sell_vote = 0

    # This function is used to monitor and detect whenever significant changes have occurred.  All strategies are
    # called from this function when a significant price has been detected.
    def monitor_price(self, data_lookback=cfg.MONITOR_DR):
        begin_date = bd.BotData().parse_time(str(datetime.utcnow() - timedelta(seconds=data_lookback)))
        date_range = (begin_date, bd.BotData().parse_time(str(datetime.utcnow())))

        max_min_index = 0
        hist_real_index = 0

        x = []
        y = []
        local_max = ([], [])
        local_min = ([], [])
        append_x = x.append
        append_y = y.append
        insert_x = x.insert
        insert_y = y.insert
        summation_y = 0

        abs_max = (begin_date, 0)
        abs_min = (begin_date, float('inf'))

        interval_time = datetime.utcnow()
        while True:
            # variable used to hold the current time
            time_stamp = datetime.utcnow()

            # checking if interval has completed
            if time_stamp >= interval_time:
                select_historical = bd.BotData().select_bitcoin_historical(date_range)
                select = bd.BotData().select_bitcoin_real_time(date_range)

                for row in select_historical:
                    values = (bd.BotData().parse_time(row[1]), float(row[2]))
                    insert_x(hist_real_index, values[0])
                    insert_y(hist_real_index, values[1])
                    summation_y += values[1]
                    hist_real_index += 1

                for row in select:
                    values = (bd.BotData().parse_time(row[1]), float(row[2]))
                    append_x(values[0])
                    append_y(values[1])

                n = hist_real_index
                if n > 0:
                    # mean and std are derived from the historical data
                    mean = summation_y / n
                    std = bd.BotData().std(bd.BotData().var(mean, y[0:hist_real_index]))
                    price = y[-1]

                    # processing data and saving results
                    poi = bd.BotData().find_poi(x[max_min_index:], y[max_min_index:], local_max, local_min, abs_max, abs_min, mean, std)
                    local_max = poi[0]
                    local_min = poi[1]
                    abs_max = poi[2]
                    abs_min = poi[3]
                    max_index = poi[4][0] + max_min_index
                    min_index = poi[4][1] + max_min_index
                    max_min_index = min(max_index, min_index) - 1

                    # checking for local max and min
                    if local_max != ([], []):
                        new_max = local_max[0][0], local_max[1][0]
                        self.price_logic(x[max_index:], y[max_index:], new_max, hist_real_index - max_index, abs_max, price, "sell")

                    if local_min != ([], []):
                        new_min = local_min[0][0], local_min[1][0]
                        self.price_logic(x[min_index:], y[min_index:], new_min, hist_real_index - min_index, abs_max, price, "buy")

                    # Graphing data
                    gd.GraphChart().graph_data(x, y, mean, std, local_max, local_min, abs_max, abs_min)

            # updating interval_time
            if time_stamp >= interval_time:
                interval_time = datetime.utcnow() + timedelta(seconds=cfg.MONITOR_R)
                date_range = (date_range[1], interval_time)

            # updating graph
            gd.GraphChart().update_graph()

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
        end_date = bd.BotData().parse_time(str(newest_point[0] + timedelta(seconds=data_lookahead)))

        print(str(x[-1]), str(end_date), x[-1] > end_date)
        if x[-1] > end_date:
            n = len(y)
            if n > 0:
                mean = newest_point[1]
                std = bd.BotData().std(bd.BotData().var(mean, y))/2

                in_std_count = 0
                real_time_weight = 1/1440
                for item in y[0:index]:
                    if mean + std > item > mean - std:
                        in_std_count += 1

                for item in y[index:]:
                    if mean + std > item > mean - std:
                        in_std_count += 1 * real_time_weight

                stability_prob = float(in_std_count) / float(n)
                print "Stability Probability: %f" % stability_prob
                gd.GraphChart().normal_graph(x, y, mean, std)
                if stability_prob > threshold:
                    return True

        return False

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