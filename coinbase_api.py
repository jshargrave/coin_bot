from coinbase.wallet.client import Client


class CoinBaseAPI:
    def __init__(self, api_key, secret_key):
        self.key = api_key
        self.secret = secret_key
        self.client = Client(self.key, self.secret)

    def get_historical_prices(self):
        return self.client.get_historic_prices()

    def get_client(self):
        return self.client.get_current_user()

    def get_accounts(self):
        return self.client.get_accounts()

    def get_buy_price(self):
        return self.client.get_buy_price(currency_pair='BTC-USD')

    def get_sell_price(self):
        return self.client.get_sell_price(currency_pair='BTC-USD')

    def get_spot_price(self):
        return self.client.get_spot_price(currency_pair='BTC-USD')

    def get_server_time(self):
        return self.client.get_time()