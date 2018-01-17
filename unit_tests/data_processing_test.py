import unittest
from data_processing import *
import datetime
import time

test_date_tuple = ("2011-09-01", "2019-09-11")


class test_data_processing_methods(unittest.TestCase):
    def setUp(self):
        self.data_p = DataProcessing()

    def test_inserting_data(self):
        # Testing all insert functions
        self.data_p.bot_d.rebuild_tables()
        self.data_p.insert_btc_rt_into_db()

        self.data_p.bot_d.rebuild_tables()
        self.data_p.insert_btc_hist_into_db_yest()

        self.data_p.bot_d.rebuild_tables()
        self.data_p.insert_btc_hist_into_db(test_date_tuple)

    def test_selecting_data(self):
        # Testing all insert functions
        self.data_p.bot_d.rebuild_tables()

        # building database
        self.data_p.insert_btc_rt_into_db()
        self.data_p.insert_btc_hist_into_db(test_date_tuple)

        # test data select
        self.data_p.select_btc_hist_range(test_date_tuple)
        self.data_p.select_btc_hist_all()

        self.data_p.select_btc_rt_range(test_date_tuple)
        self.data_p.select_btc_rt_all()

    def test_graphing(self):
        # Testing all insert functions
        self.data_p.bot_d.rebuild_tables()
        self.data_p.insert_btc_hist_into_db(test_date_tuple)

        data_range = ("2017-11-07", "2018-01-10")
        t_delta = datetime.timedelta(days=5)

        self.data_p.graph_data_bh_range(data_range)
        self.data_p.graph_data_bh_range_max(data_range, t_delta)
        self.data_p.graph_data_bh_range_min(data_range, t_delta)
        time.sleep(5)


    def test_average_calculation(self):
        self.data_p.bot_d.rebuild_tables()
        self.data_p.insert_btc_hist_into_db(test_date_tuple)

        data_range = ("2018-10-01", "2018-01-01")
        select_gen = self.data_p.select_btc_hist_range(data_range)
        avg = self.data_p.calculate_average(select_gen)

    def test_datetime_methods(self):
        # parse date string
        str_date = "2017-10-01"
        new_date = self.data_p.convert_str_to_datetime(str_date)

        new_date = self.data_p.datetime_diff(new_date, days=10)

    def test_local_max_min(self):
        self.data_p.bot_d.rebuild_tables()
        self.data_p.insert_btc_hist_into_db(test_date_tuple)
        t_delta = datetime.timedelta(days=5)

        select_gen = self.data_p.select_btc_hist_all()
        for i in self.data_p.local_max_generator(select_gen, t_delta):
            pass

        select_gen = self.data_p.select_btc_hist_all()
        for i in self.data_p.local_min_generator(select_gen, t_delta):
            pass

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()