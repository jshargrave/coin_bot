import os
import json


class BotTrade:
    def __init__(self, balance_file="data\\balance.json", trade_file="data\\trade.json"):
        self.balance_file = balance_file
        self.trade_file = trade_file
        self._balance = self.get_balance()
        self._trade_list = self.get_trade()


        self.save_all()

    def get_balance(self):
        # If no balance file exist, then load default balance
        if not os.path.exists(self.balance_file):
            return self.default_balance()

        # Read and return json value
        with open(self.balance_file, 'r') as infile:
            file_str = infile.read()

        json_parsed = json.loads(file_str)
        return json_parsed

    @staticmethod
    def default_balance():
        return {"USD": 0, "BTC": 0}

    def get_trade(self):
        # If no balance file exist, then load default balance
        if not os.path.exists(self.trade_file):
            return self.default_trade()

        # Read and return json value
        with open(self.trade_file, 'r') as infile:
            file_str = infile.read()

        json_parsed = json.loads(file_str)
        return json_parsed

    @staticmethod
    def default_trade():
        return []

    def save_all(self):
        self.save_balance()
        self.save_trade()

    def save_balance(self):
        with open(self.balance_file, 'w') as outfile:
            json.dump(self._balance, outfile)

    def save_trade(self):
        with open(self.trade_file, 'w') as outfile:
            json.dump(self._trade_list, outfile)
