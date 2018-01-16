import unittest
from coin_desk_api import *

test_date_tuple = ("2013-09-01", "2013-09-11")


class test_coin_desk_api_methods(unittest.TestCase):
    def setUp(self):
        self.cd = CoinDeskAPI()

    def test_get_btc_price(self):
        data = self.cd.get_btc_price()
        self.assertTrue(self.cd.r.status_code == 200)
        self.assertTrue(isinstance(data[0], str))
        self.assertTrue(isinstance(data[1], float))

    def test_get_yesterdays_btc_price(self):
        data = self.cd.get_btc_yesterdays_price()
        self.assertTrue(self.cd.r.status_code == 200)
        self.assertTrue(isinstance(data[0], str))
        self.assertTrue(isinstance(data[1], float))

    def test_get_historical_btc_price(self):
        data = self.cd.get_btc_hist_price_range(test_date_tuple)
        self.assertTrue(self.cd.r.status_code == 200)

    def test_historical_generator(self):
        for x, y in self.cd.btc_hist_price_generator(test_date_tuple):
            pass

    def test_convert_data(self):
        self.cd.get_btc_hist_db_data(test_date_tuple)


if __name__ == '__main__':
    unittest.main()
