import bot_strategy
from multiprocessing import Process
import config as cfg

import datetime as dt

from coin_desk_api import CoinDeskAPI
from bot_data import BotData
from moving_avg import MovingAverage


def main():
    # Creating dictionary for data retrieving
    data_dict = {"BTC_Historical": CoinDeskAPI().get_btc_hist_db_data}

    # Creating database for data
    database = BotData(data_dict)

    # Creating moving average
    moving_avg = MovingAverage(database.select_bh_range, dt.timedelta(days=10000), dt.timedelta(days=100))

    for i in moving_avg.calculate_simple_moving_average():
        print(i)


if __name__ == '__main__':
    main()
