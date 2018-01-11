import requests

current_btc_price_url = "https://api.coindesk.com/v1/bpi/currentprice.json"
historical_btc_price_url = "https://api.coindesk.com/v1/bpi/historical/close.json?start={}&end={}"


class CoinDeskAPI:
    def __init__(self):
        self.r = requests
    '''
      gets the current btc price and returns a float
    '''
    def get_btc_price(self):
        self.r = requests.get(current_btc_price_url)
        date = self.r.json()['time']['updatedISO']
        price = self.r.json()['bpi']['USD']['rate_float']
        return self.convert_date_rt_btc(date), price


    '''
      returns the historical prices of btc over the date_range (start date, end date) in json.  date_range is a tuple 
      starting with the start date and then the end date.  dates should be formatted such that YYYY-MM-DD.  
    '''
    def get_btc_hist_price(self, date_range):
        url = historical_btc_price_url.format(*date_range)
        self.r = requests.get(url)
        return self.r.json()['bpi']

    '''
      Generator for reading through the contents of btc historical prices.  Yields the key (date) and value 
      (price of btc) after each iteration.
    '''
    def btc_hist_price_generator(self, date_range):
        for x, y in self.get_btc_hist_price(date_range).items():
            yield x, y

    '''
      Uses the btc_generator function to return a array of tuples to be used to insert into a database.  Returns an 
      array of tuples [(key, value)] of the date and price.
    '''
    def get_btc_hist_db_data(self, data_range):
        data_list = []
        for x, y in self.btc_hist_price_generator(data_range):
            data_list.append((self.convert_date_hist_btc(x), y))
        return data_list

    def convert_date_rt_btc(self, date_str):
        return date_str[:-6].replace("T", " ")

    def convert_date_hist_btc(self, date_str):
        return "{} 00:00:00".format(date_str)

