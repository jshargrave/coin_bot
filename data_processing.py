from bot_data import *
from coin_desk_api import *
from graph_data import *


class DataProcessing:
    def __init__(self):
        self.bot_d = BotData()
        self.cd_api = CoinDeskAPI()
        self.graph_d = GraphData()

    '''
      Inserts btc realtime price into database real time table.
    '''
    def insert_btc_rt_into_db(self):
        self.bot_d.insert_brt([self.cd_api.get_btc_price()])

    '''
      Inserts btc yesterdays historical price into the database historical table.
    '''
    def insert_btc_hist_into_db_yest(self):
        self.bot_d.insert_bh([self.cd_api.get_btc_yesterdays_price()])

    '''
      Inserts btc historical data into database historical table based on the data range.
    '''
    def insert_btc_hist_into_db(self, data_range):
        self.bot_d.insert_bh(self.cd_api.get_btc_hist_db_data(data_range))

    '''
      Passes a generator function to the graphing function in the graph_data file.
    '''
    def graph_data_bh_range(self, data_range):
        self.graph_d.graph_data(self.bot_d.select_bh_range(data_range))







