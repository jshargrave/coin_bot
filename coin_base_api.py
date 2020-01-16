from coinbase.wallet.client import Client
import requests
import json


class CoinBaseAPI(Client):
    def __init__(self, api_key, secret_key):
        # Call super class constructor
        super(CoinBaseAPI, self).__init__(api_key, secret_key)

        # Save variables
        self.key = api_key
        self.secret = secret_key

        self.accounts = self.get_accounts()

    @staticmethod
    def get_historical_price(coin, date):
        payload = {'date': date}
        r = requests.get('https://api.coinbase.com/v2/prices/'+coin+'-USD/spot', params=payload)
        return r.json()['data']['amount']

    @staticmethod
    def get_price(coin):
        r = requests.get('https://api.coinbase.com/v2/prices/'+coin+'-USD/spot?currency=USD')
        return r.json()['data']['amount']

    def parse_accounts(self):
        return json.dumps(self.accounts.data)

    def parse_accounts_balance(self):
        account_balance = {}
        for account in self.accounts.data:
            account_balance[account.currency] = account.balance.amount
        return account_balance

    def refresh_all(self):
        self.accounts.refresh()
