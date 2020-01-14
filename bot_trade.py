import os
import json
import datetime


class BotTrade:
    def __init__(self, coin_price_dict, balance_file="data\\balance.json", trade_file="data\\trade.json", simulated=True):
        self._coin_price_dict = coin_price_dict
        self._balance_file = balance_file
        self._trade_file = trade_file
        self._balance = self.get_balance()
        self._trade_list = self.get_trade()
        self._simulated = simulated

        self.save_all()

    def get_balance(self):
        # If no balance file exist, then load default balance
        if not os.path.exists(self._balance_file):
            return self.default_balance()

        # Read and return json value
        with open(self._balance_file, 'r') as infile:
            file_str = infile.read()

        json_parsed = json.loads(file_str)
        return json_parsed

    @staticmethod
    def default_balance():
        return {
            "USD": 0,
            "BTC": 0,
            "Trade Count": 0
        }

    def get_trade(self):
        # If no balance file exist, then load default balance
        if not os.path.exists(self._trade_file):
            return self.default_trade()

        # Read and return json value
        with open(self._trade_file, 'r') as infile:
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
        with open(self._balance_file, 'w') as outfile:
            json.dump(self._balance, outfile, indent=4, sort_keys=True)

    def save_trade(self):
        with open(self._trade_file, 'w') as outfile:
            trade_sorted = sorted(self._trade_list, key=lambda k: k['Time'], reverse=True)
            json.dump(trade_sorted, outfile, indent=4, sort_keys=True)

    def buy_coin(self, coin, amount, max_cost=-1):
        coin_price = self._coin_price_dict[coin]()
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
            "Trade number": self._balance["Trade Count"],
            "Coin": coin,
            "Buy Price": coin_price,
            "Amount": amount,
            "Total Cost": total_cost,
            "Time": str(datetime.datetime.now())
        }
        self._trade_list.append(trade_data)
        self._balance[coin] += amount
        self._balance["USD"] -= total_cost
        self._balance["Trade Count"] += 1
        self.save_all()

    def sell_coin(self, trade_data):
        coin = trade_data["Coin"]
        coin_price = self._coin_price_dict[coin]()
        total_sell = coin_price * trade_data["Amount"]

        # Make sure we are making a profit when selling
        if total_sell < trade_data["Total Cost"]:
            print("Could not sell coin ({}) because Total Sell Price ({}) is less than Total Cost ({})".format(coin, total_sell, trade_data["Total Cost"]))
            return

        self._trade_list.remove(trade_data)
        self._balance[trade_data["Coin"]] -= trade_data["Amount"]
        self._balance["USD"] += total_sell
        self.save_all()
