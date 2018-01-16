import unittest
from data_processing import *

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


    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()