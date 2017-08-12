import requests

class CoinBaseAPI:
    def __init__(self, api_key, secret_key):
        self.key = api_key
        self.secret = secret_key

    def get_historical_prices(self, date, coin):
        payload = {'date': date}
        r = requests
        for i in range(400):
            r = requests.get('https://api.coinbase.com/v2/prices/'+coin+'-USD/spot', params=payload)
        return r.json()['data']['amount']

    def get_price(self, coin):
        r = requests.get('https://api.coinbase.com/v2/prices/'+coin+'-USD/spot?currency=USD')
        return r.json()['data']['amount']