import os
import json
import datetime


class BotTrade:
    def __init__(self, balance_file="data\\balance.json", trade_file="data\\trade.json", simulated=True):
        self.balance_file = balance_file
        self.trade_file = trade_file
        self._balance = self.get_balance()
        self._trade_list = self.get_trade()
        self.simulated = simulated
        self.trade_count = len(self._trade_list)


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
            json.dump(self._balance, outfile, indent=4, sort_keys=True)

    def save_trade(self):
        with open(self.trade_file, 'w') as outfile:
            trade_sorted = sorted(self._trade_list, key=lambda k: k['Time'], reverse=True)
            json.dump(trade_sorted, outfile, indent=4, sort_keys=True)

    def buy_coin(self, coin, coin_price, amount, max_cost=-1):
        total_cost = coin_price * amount

        # Make sure total cost is not more than max cost
        if max_cost != -1 and max_cost < total_cost:
            print("Could not buy coin ({}) because Total Cost ({}) is more than Max Cost ({}).".format(coin, total_cost, max_cost))
            return

        # Make sure enough USD in balance
        if self._balance["USD"] < total_cost:
            print("Could not buy coin ({}) because USD Balance ({}) is less than Total Cost ({})".format(coin, self._balance["USD"], total_cost))
            return

        trade_data = {
            "Trade number": self.trade_count,
            "Coin": coin,
            "Buy Price": coin_price,
            "Amount": amount,
            "Total Cost": total_cost,
            "Time": str(datetime.datetime.now())
        }
        self._trade_list.append(trade_data)
        self._balance[coin] += amount
        self._balance["USD"] -= total_cost
        self.trade_count += 1
        self.save_all()
