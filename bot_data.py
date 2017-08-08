from dateutil.parser import *
from datetime import *
import config as cfg
import bot_api as ba
import sqlite3
import csv
import math


# dates used in database query should be formatted as "YYYY-MM-DD HH:MM:SS"
class BotData:
    def __init__(self):
        self.conn = sqlite3.connect('BotData.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS BitcoinHistorical(id integer PRIMARY KEY, date text NOT NULL, "
                            "avg real NOT NULL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS BitcoinRealTime(id integer PRIMARY KEY, date text NOT NULL, "
                            "price real NOT NULL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS BitcoinTrans(id integer PRIMARY KEY, date text NOT NULL, "
                            "amount real NOT NULL, price real NOT NULL)")

    def monitor_data(self, refresh=cfg.BD_MONITOR_R):
        minute = datetime.utcnow().minute
        day = datetime.utcnow().day

        while True:
            # variable used to hold the current time
            now_min = datetime.utcnow().minute
            now_day = datetime.utcnow().day

            # daily data
            if day == now_day:
                print("Getting historical data and inserting...")
                historical = ba.CoinBaseAPI(cfg.API_KEY, cfg.API_SECRET).get_historical_prices().prices
                insert_array = []

                for item in historical:
                    insert_array.insert(0, (self.parse_time(item.time), float(item.price)))

                self.drop_bitcoin_historical()
                self.drop_bitcoin_real_time()
                self.insert_bitcoin_historical(insert_array)
                print("Completed")

            # real time data
            if minute == now_min:
                time_stamp = self.parse_time(str(datetime.utcnow()))
                insert_array = []

                # insert price
                price = self.get_coinbase_price()
                insert_array.append((time_stamp, price))
                self.insert_bitcoin_real_time(insert_array)
                print(str(time_stamp), price)

            # updating interval_time
            if minute <= now_min:
                minute = (datetime.utcnow() + timedelta(minutes=refresh)).minute

            if day <= now_day:
                day = (datetime.utcnow() + timedelta(days=1)).day

    def rebuild_tables(self):
        print("Clearing all tables...")
        self.cursor.execute("DROP TABLE BitcoinHistorical")
        self.cursor.execute("DROP TABLE BitcoinRealTime")
        self.cursor.execute("DROP TABLE BitcoinTrans")
        self.__init__()
        print("Completed")

    def drop_bitcoin_historical(self):
        self.cursor.execute("DROP TABLE BitcoinHistorical")
        self.__init__()
        print("Dropped BitcoinHistorical table.")

    def drop_bitcoin_real_time(self):
        self.cursor.execute("DROP TABLE BitcoinRealTime")
        self.__init__()
        print("Dropped BitcoinRealTime table.")

    # ----------------------------------------------- Insert Commands ------------------------------------------
    def insert_bitcoin_historical(self, array_tuple):
        self.cursor.executemany("INSERT INTO BitcoinHistorical(date, avg) VALUES (?,?)", array_tuple)
        self.conn.commit()

    def insert_bitcoin_real_time(self, array_tuple):
        self.cursor.executemany("INSERT INTO BitcoinRealTime(date, price) VALUES (?,?)", array_tuple)
        self.conn.commit()

    def insert_bitcoin_transactions(self, array_tuple):
        self.cursor.executemany("INSERT INTO BitcoinTrans(date, amount, price) VALUES (?,?,?)", array_tuple)
        self.conn.commit()

    # ------------------------------------------- Select Commands ------------------------------------------------
    def select_bitcoin_historical(self, date_range):
        self.cursor.execute("SELECT * FROM BitcoinHistorical WHERE date >= ? and date <= ?", date_range)
        return self.cursor.fetchall()

    def select_bitcoin_historical_all(self):
        self.cursor.execute("SELECT * FROM BitcoinHistorical")
        return self.cursor.fetchall()

    def select_bitcoin_real_time(self, date_range):
        self.cursor.execute("SELECT * FROM BitcoinRealTime WHERE date >= ? and date <= ?", date_range)
        return self.cursor.fetchall()

    def select_bitcoin_real_time_all(self):
        self.cursor.execute("SELECT * FROM BitcoinRealTime")
        return self.cursor.fetchall()

    # -------------------------------------------- Data Processing Functions -----------------------------------
    def process_data_bitcoinity(self, file_path):
        read_file = open(file_path, 'r')
        csv_reader = csv.reader(read_file)

        data = []
        next(csv_reader, None)
        for row in csv_reader:
            data_line = (self.parse_time(row[0]), float(row[1]))
            data.append(data_line)

        read_file.close()
        self.insert_bitcoin_historical(data)

    def process_data_kaggle(self, file_path):
        print("Reading in Kaggle dataset...")
        read_file = open(file_path, 'r')
        csv_reader = csv.reader(read_file)

        data = []
        count = 0
        next(csv_reader, None)
        for row in csv_reader:
            if "NaN" in row:
                continue
            count += 1

            time_stamp = datetime.utcfromtimestamp(float(row[0]))
            data_line = (str(time_stamp), (float(row[2]) + float(row[3]))/2)
            data.append(data_line)

        self.insert_bitcoin_historical(data)
        print "Completed: %.0f items inserted." % count
        read_file.close()

    def parse_time(self, time_stamp):
        new_time = parse(time_stamp).replace(microsecond=0).replace(tzinfo=None)
        return new_time

    def increment_date(self, date, d=0, h=0, s=0, ms=0):
        return date + timedelta(days=d, hours=h, seconds=s, microseconds=ms)

    def decrement_date(self, date, d=0, h=0, s=0, ms=0):
        return date - timedelta(days=d, hours=h, seconds=s, microseconds=ms)

    def get_coinbase_price(self):
        return float(ba.CoinBaseAPI(cfg.API_KEY, cfg.API_SECRET).get_price().amount)

    def find_poi(self, x, y, local_max, local_min, abs_max, abs_min, mean, std, time_limit=cfg.POI_TL):
        n = len(x)
        value_increase = False
        value_decrease = False
        max_index = []
        min_index = []

        for i in range(n):
            if y[i] > abs_max[1]:
                abs_max = (x[i], y[i])
            if y[i] < abs_min[1]:
                abs_min = (x[i], y[i])
            if i == 0:
                continue
            if i == n - 1:
                continue

            # values are increasing
            if y[i - 1] < y[i]:
                # potential dip found
                if value_decrease:
                    value_decrease = False
                    data_range = self.decrement_date(self.parse_time(str(x[i - 1])), s=time_limit)
                    add_index = True
                    # adding dip logic
                    if len(min_index) > 0:
                        if x[min_index[0]] >= data_range:
                            if y[i - 1] >= y[min_index[0]]:
                                add_index = False
                            elif y[i - 1] < y[min_index[0]]:
                                del min_index[0]

                    if add_index and y[i - 1] < mean - std:
                        min_index.insert(0, i - 1)

                value_increase = True

            # values are decreasing
            if y[i - 1] > y[i]:
                # potential peak found
                if value_increase:
                    value_increase = False
                    data_range = self.decrement_date(self.parse_time(str(x[i - 1])), s=time_limit)
                    add_index = True
                    # adding peak logic
                    if len(max_index) > 0:
                        if x[max_index[0]] >= data_range:
                            if y[i - 1] <= y[max_index[0]]:
                                add_index = False
                            if y[i - 1] > y[max_index[0]]:
                                del max_index[0]

                    if add_index and y[i - 1] > mean + std:
                        max_index.insert(0, i - 1)

                value_decrease = True

        # local_min and local_max are empty (first time running poi), therefore remove the last elm and append
        if local_min != ([], []) and local_max != ([], []):
            del local_max[0][-1]
            del local_max[1][-1]
            del local_min[0][-1]
            del local_min[1][-1]

        for max_i in reversed(max_index):
            local_max[0].append(x[max_i])
            local_max[1].append(y[max_i])

        for min_i in reversed(min_index):
            local_min[0].append(x[min_i])
            local_min[1].append(y[min_i])

        if len(max_index) == 0 and len(min_index) == 0:
            index = (0, 0)
        elif len(max_index) == 0:
            index = (0, min_index[0])
        elif len(min_index) == 0:
            index = (max_index[0], 0)
        else:
            index = (max_index[0], min_index[0])

        return local_max, local_min, abs_max, abs_min, index

    def var(self, mean, data):
        sum_data = 0
        n = len(data)
        for d in data:
            diff = d - mean
            sum_data += diff*diff
        return sum_data/n

    def std(self, var):
        return math.sqrt(var)