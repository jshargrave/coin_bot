import bot_data as bd


class BotStrategy():

    # Running average works by computeing the running average of a set amount of historical time.  If the average is
    # increasing, we invest.  If the average is decreasing, we sell.
    def running_avg_strategy(self):
        pass

    # The stability approach works by investing only during stable prices.  This is a more long term approach, that
    # assumes prices will stagnate, and then become noising again.
    def stability_strategy(self):
        pass

    # The potential gain approach works by using the absolute max/min as a proof of concept.  Comparing the current
    # price with what is can be in the future.
    def potential_gain_strategy(self):
        pass

    # The linear regression strategy works by computing two linear regressions, one over a longer peroid of data, and
    # one over a shorter period of data.  We can then compare the two, and based on the diffrences we can decide to buy
    # or sell.
    def linear_regression_strategy(self):
        pass