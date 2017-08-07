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
    def monitor_price(self, data_lookback=cfg.MONITOR_DR):
        begin_date = bd.BotData().parse_time(str(datetime.utcnow() - timedelta(seconds=data_lookback)))
        date_range = (begin_date, bd.BotData().parse_time(str(datetime.utcnow())))

        x_hist = []
        y_hist = []
        x = []
        y = []

        minute = datetime.utcnow().minute
        while True:
            # variable used to hold the current time
            now_min = datetime.utcnow().minute

            # checking if interval has completed
            if minute == now_min:
                select_historical = bd.BotData().select_bitcoin_historical(date_range)
                select = bd.BotData().select_bitcoin_real_time(date_range)

                for row in select_historical:
                    values = (bd.BotData().parse_time(row[1]), float(row[2]))
                    y_hist.append(values[1])
                    x_hist.append(values[0])

                for row in select:
                    values = (bd.BotData().parse_time(row[1]), float(row[2]))
                    y.append(values[1])
                    x.append(values[0])

                n = len(y_hist)
                if n > 0:
                    # mean and std are derived from the historical data
                    mean = (sum(y_hist)) / n
                    std = bd.BotData().std(bd.BotData().var(mean, y_hist))
                    price = y[-1]

                    # Processing Data
                    print(n)
                    local_maximums = bd.BotData().calculate_local_max(x_hist + x, y_hist + y, int(n * cfg.MONITOR_LA_PER) + 1, std)
                    local_minimums = bd.BotData().calculate_local_min(x_hist + x, y_hist + y, int(n * cfg.MONITOR_LA_PER) + 1, std)
                    absolute_max = bd.BotData().find_absolute_max(x_hist + x, y_hist + y)
                    absolute_min = bd.BotData().find_absolute_min(x_hist + x, y_hist + y)

                    # Graphing data
                    gd.GraphChart().graph_data(x_hist + x, y_hist + y, local_maximums, local_minimums, absolute_max, absolute_min, price, mean, std)

                    newest_max = local_maximums[0][0], local_maximums[1][0]
                    newest_min = local_minimums[0][0], local_minimums[1][0]

                    if self.is_price_stable(newest_max):
                        pass

                    if self.is_price_stable(newest_min):
                        pass

            # updating interval_time
            if minute <= now_min:
                minute = (datetime.utcnow() + timedelta(minutes=cfg.MONITOR_R)).minute
                date_range = (date_range[1], datetime.utcnow() + timedelta(minutes=cfg.MONITOR_R))

            # updating graph
            gd.GraphChart().update_graph()

    # Running average works by computing the running average of a set amount of historical time.  If the average is
    # increasing, we invest.  If the average is decreasing, we sell.
    def running_avg_strategy(self):
        pass

    # The stability approach works by investing only during stable prices.  This is a more long term approach, that
    # assumes prices will stagnate, and then become noising again.
    def is_price_stable(self, newest_point, data_lookahead=cfg.STABLE_LA, threshold=cfg.STABLE_T):
        begin_date = newest_point[0]
        end_date = bd.BotData().parse_time(str(begin_date + timedelta(seconds=data_lookahead)))
        date_range = (begin_date, end_date)

        x = []
        y = []

        if datetime.utcnow() > begin_date:
            select_historical = bd.BotData().select_bitcoin_historical(date_range)
            select = bd.BotData().select_bitcoin_real_time(date_range)

            for row in select_historical:
                values = (bd.BotData().parse_time(row[1]), float(row[2]))
                y.append(values[1])
                x.append(values[0])

            for row in select:
                values = (bd.BotData().parse_time(row[1]), float(row[2]))
                y.append(values[1])
                x.append(values[0])

            n = len(y)
            if n > 0:
                mean = sum(y)/n
                std = bd.BotData().std(bd.BotData().var(mean, y))

                in_std_count = 0
                for item in y:
                    if item < mean + std/2 and item > mean - std/2:
                        in_std_count += 1

                stability_prob = float(in_std_count) / float(n)
                print "Stability Probability: %.2f" % stability_prob
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