import unittest
from data_processing import *
from graph_data import *
import time

test_date_tuple = ("2010-07-17", "2019-01-11")
test_data = [
             ("2007-08-21 10:01:10", 1.0),
             ("2007-08-27 10:01:10", 1000.0),
             ("2007-08-28 10:01:10", 500.0),
             ("2007-08-22 10:01:10", 600.0),
             ("2007-08-26 10:01:10", 650.0),
             ("2007-08-29 10:01:10", 345.0),
             ("2007-08-30 10:01:10", 1034.0)
            ]


class test_graph_data_methods(unittest.TestCase):
    def setUp(self):
        self.data_p = DataProcessing()
        self.data_p.bot_d.rebuild_tables()
        self.data_p.insert_btc_rt_into_db()
        self.data_p.insert_btc_hist_into_db(test_date_tuple)

        self.graph_d = GraphData()


    def test_update_graph(self):
        self.graph_d.graph_data(self.data_p.bot_d.select_bh_range(("2017-11-01", "2019-01-01")))
        time.sleep(5)

    def data_generator(self):
        for i in test_data:
            yield i

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()