import requests
import datetime_funcs


class CouldNotGetBTCHistoricalPrice(ValueError): pass


current_btc_price_url = "https://api.coindesk.com/v1/bpi/currentprice.json"
historical_btc_price_url = "https://api.coindesk.com/v1/bpi/historical/close.json?start={}&end={}"
yesterdays_btc_price_url = "https://api.coindesk.com/v1/bpi/historical/close.json?for=yesterday"


class CoinDeskAPI:
    def __init__(self):
        self.r = requests
    '''
      gets the current btc price and returns a tuple (date, price)
    '''
    def get_btc_price(self):
        self.r = requests.get(current_btc_price_url)
        date = self.r.json()['time']['updatedISO']
        price = self.r.json()['bpi']['USD']['rate_float']
        return datetime_funcs.get_current_date(), price

    def get_btc_yesterdays_price(self):
        self.r = requests.get(yesterdays_btc_price_url)
        data = [(k, v) for k, v in self.r.json()['bpi'].items()][0]
        return data

    '''
      returns the historical prices of btc over the date_range (start date, end date) in json.  date_range is a tuple 
      starting with the start date and then the end date.  dates should be formatted such that YYYY-MM-DD.  
    '''
    def get_btc_hist_price_range(self, date_range):
        try:
            url = historical_btc_price_url.format(*date_range)
            self.r = requests.get(url)
            return self.r.json()['bpi']
        except ValueError as e:
            raise CouldNotGetBTCHistoricalPrice("Failed to get btc historical price range!\n{}".format(self.r.text))


    '''
      Generator for reading through the contents of btc historical prices.  Yields the key (date) and value 
      (price of btc) after each iteration.
    '''
    def btc_hist_price_generator(self, date_range):
        for x, y in self.get_btc_hist_price_range(date_range).items():
            yield x, y

    '''
      This function should be used to return an array tuple to insert into a database.
      
      Uses the btc_generator function to return a array of tuples to be used to insert into a database.  Returns an 
      array of tuples [(key, value)] of the date and price.
    '''
    def get_btc_hist_db_data(self, data_range):
        data_list = []
        for x, y in self.btc_hist_price_generator(data_range):
            data_list.append((self.convert_date_hist_btc(x), y))
        return data_list

    @staticmethod
    def convert_date_rt_btc(date_str):
        return date_str[:-6].replace("T", " ")

    @staticmethod
    def convert_date_hist_btc(date_str):
        return datetime_funcs.add_time_format(date_str)

