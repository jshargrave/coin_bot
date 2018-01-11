import os
import unittest
from bot_data import *
from coin_desk_api import *

test_db = "test.db"
test_data = [
             ("2007-08-21 10:01:10", 1.0),
             ("2007-08-27 10:01:10", 1000.0),
             ("2007-08-28 10:01:10", 500.0),
             ("2007-08-22 10:01:10", 600.0),
             ("2007-08-26 10:01:10", 650.0),
             ("2007-08-29 10:01:10", 345.0),
             ("2007-08-30 10:01:10", 1034.0)
            ]
test_date_tuple = ("2011-09-01", "2019-09-11")


class test_bot_data_methods(unittest.TestCase):
    def setUp(self):
        self.bd = BotData(test_db)

    # Makes sure the database can rebuild itself after clearing all tables
    def test_rebuild_database(self):
        self.bd.rebuild_tables()

    # Checks the insert function for each table
    def test_database_insert(self):
        # Rebuilding Database
        self.bd.rebuild_tables()

        # Inserting into BitcoinHistorical table
        self.bd.insert_bh(test_data)

        # Inserting into BitcoinRealTime table
        self.bd.insert_brt(test_data)

    # Check that delete functions are working
    def test_database_delete(self):
        # Rebuilding Database
        self.bd.rebuild_tables()

        # Inserting into BitcoinHistorical table
        self.bd.insert_bh(test_data)

        # Inserting into BitcoinRealTime table
        self.bd.insert_brt(test_data)

        # Deleting from BitcoinHistorical table
        self.bd.delete_where_bh("id = 1")

        # Deleting from BitcoinRealTime table
        self.bd.delete_where_brt("id = 2")

    # Test all the select functions
    def test_database_select(self):
        self.bd.rebuild_tables()

        # Inserting into BitcoinHistorical table
        self.bd.insert_bh(test_data)

        # Inserting into BitcoinRealTime table
        self.bd.insert_brt(test_data)

        # btc historical all select
        for i in self.bd.select_bh_all():
            pass

        # btc historical range select
        for i in self.bd.select_bh_range(test_date_tuple):
            pass

        # btc real time all select
        for i in self.bd.select_brt_all():
            pass

        # btc real time range select
        for i in self.bd.select_brt_range(test_date_tuple):
            pass

    def test_coin_desk_insert_historical(self):
        self.bd.rebuild_tables()
        cd = CoinDeskAPI()

        # inserting historical data
        data = cd.get_btc_hist_db_data(test_date_tuple)
        self.bd.insert_bh(data)

    def test_coin_desk_insert_real_time(self):
        self.bd.rebuild_tables()
        cd = CoinDeskAPI()

        # getting real-time data
        data = [cd.get_btc_price()]

        # inserting data
        self.bd.insert_brt(data)

    def tearDown(self):
        os.remove(test_db)


if __name__ == '__main__':
    unittest.main()
