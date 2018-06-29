import requests


class CoinBaseAPI:
    def __init__(self, api_key, secret_key):
        self.key = api_key
        self.secret = secret_key

    @staticmethod
    def get_historical_price(coin, date):
        payload = {'date': date}
        r = requests.get('https://api.coinbase.com/v2/prices/'+coin+'-USD/spot', params=payload)
        return r.json()['data']['amount']

    @staticmethod
    def get_price(coin):
        r = requests.get('https://api.coinbase.com/v2/prices/'+coin+'-USD/spot?currency=USD')
        return r.json()['data']['amount']