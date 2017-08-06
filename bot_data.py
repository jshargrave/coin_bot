from dateutil.parser import *
from datetime import *
import config as cfg
import bot_api as ba
import sqlite3
import csv
import sys
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

    def rebuild_tables(self):
        print("Clearing all tables...")
        self.cursor.execute("DROP TABLE BitcoinHistorical")
        self.cursor.execute("DROP TABLE BitcoinRealTime")
        self.cursor.execute("DROP TABLE BitcoinTrans")
        self.__init__()
        print("Completed")

    # ----------------------------------------------- Insert Commands ------------------------------------------
    def insert_into_bitcoin_historical(self, array_tuple):
        self.cursor.executemany("INSERT INTO BitcoinHistorical(date, avg) VALUES (?,?)", array_tuple)
        self.conn.commit()

    def insert_into_real_time(self, array_tuple):
        self.cursor.executemany("INSERT INTO BitcoinRealTime(date, price) VALUES (?,?)", array_tuple)
        self.conn.commit()

    def insert_into_bitcoin_transactions(self, array_tuple):
        self.cursor.executemany("INSERT INTO BitcoinTrans(date, amount, price) VALUES (?,?,?)", array_tuple)
        self.conn.commit()

    # ------------------------------------------- Select Commands ------------------------------------------------
    def select_bitcoin_historical(self, date_range):
        self.cursor.execute("SELECT * FROM BitcoinHistorical WHERE date >= ? and date <= ?", date_range)
        return self.cursor.fetchall()

    def select_bitcoin_real_time(self, date_range):
        self.cursor.execute("SELECT * FROM BitcoinRealTime WHERE date >= ? and date <= ?", date_range)
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
        self.insert_into_bitcoin_historical(data)

    def process_data_kaggle(self, file_path):
        read_file = open(file_path, 'r')
        csv_reader = csv.reader(read_file)

        data = []
        next(csv_reader, None)
        for row in csv_reader:
            if "NaN" in row:
                continue

            time_stamp = datetime.utcfromtimestamp(float(row[0]))
            data_line = (str(time_stamp), (float(row[2]) + float(row[3]))/2)
            data.append(data_line)

        self.insert_into_bitcoin_historical(data)
        read_file.close()

    def parse_time(self, time_stamp):
        new_time = parse(time_stamp).replace(microsecond=0).replace(tzinfo=None)
        return new_time

    def retrieve_data(self, min):
        api_list = [ba.CoinBaseAPI(cfg.API_KEY, cfg.API_SECRET)]

        # initial time_stamp
        interval_time = datetime.utcnow().replace(second=0, microsecond=0)

        while True:
            # variable used to hold the current time
            now_time = datetime.utcnow().replace(second=0, microsecond=0)

            # checking if interval has completed
            if interval_time == now_time:
                insert_array = []
                time_stamp = self.parse_time(str(datetime.utcnow()))

                # getting all prices from api list
                for api in api_list:
                    price = float(api.get_price().amount)
                    insert_array.append((time_stamp, price))

                # inserting values into database
                self.insert_into_real_time(insert_array)
                sys.stdout.write('.')
                sys.stdout.flush()

            # updating interval_time
            if interval_time <= now_time:
                interval_time = now_time + timedelta(minutes=min)

    def calculate_local_max(self, x, y, look_ahead, std):
        n = len(y)
        local_max_x = []
        local_max_y = []
        mean = sum(y) / len(y)

        # note don't index anything less then 0 and greater than n - 1
        i = 0
        while i < n:
            # value to inspect
            value = y[i]
            l_condition, r_condition = True, True

            # check left side
            l_count = 0
            while l_count < look_ahead:
                index = i - l_count - 1
                if index < 0:
                    break

                # if there is a point > than the value or value is not > std + mean, not local max
                if y[index] > value or value <= mean + std:
                    l_condition = False
                    break
                l_count += 1

            # check right side
            r_count = 0
            while r_count < look_ahead:
                index = i + r_count + 1
                if index > n - 1:
                    break

                # if there is a point > than the value or value is not > std + mean, not local max
                if y[index] > value or value <= mean + std:
                    r_condition = False
                    break
                r_count += 1

            # checking if local maximum conditions were met
            if l_condition and r_condition:
                local_max_x.append(x[i])
                local_max_y.append(y[i])

            i += 1

        return local_max_x, local_max_y

    def calculate_local_min(self, x, y, look_ahead, std):
        n = len(y)
        local_min_x = []
        local_min_y = []
        mean = sum(y) / len(y)

        # note don't index anything less then 0 and greater than n - 1
        i = 0
        while i < n:
            # value to inspect
            value = y[i]
            l_condition, r_condition = True, True

            # check left side
            l_count = 0
            while l_count < look_ahead:
                index = i - l_count - 1
                if index < 0:
                    break

                # if there is a point < than the value or value is not < std - mean, not local min
                if y[index] < value or value > mean - std:
                    l_condition = False
                    break
                l_count += 1

            # check right side
            r_count = 0
            while r_count < look_ahead:
                index = i + r_count + 1
                if index > n - 1:
                    break

                # if there is a point < than the value or value is not < std - mean, not local min
                if y[index] < value or value > mean - std:
                    r_condition = False
                    break
                r_count += 1

            # checking if local maximum conditions were met
            if l_condition and r_condition:
                local_min_x.append(x[i])
                local_min_y.append(y[i])

            i += 1

        return local_min_x, local_min_y

    def find_absolute_max(self, x, y):
        n = len(y)
        max_value = y[0]
        max_date = x[0]

        for i in range(n):
            if y[i] > max_value:
                max_value = y[i]
                max_date = x[i]

        return max_date, max_value

    def find_absolute_min(self, x, y):
        n = len(y)
        min_value = y[0]
        min_date = x[0]

        for i in range(n):
            if y[i] < min_value:
                min_value = y[i]
                min_date = x[i]

        return min_date, min_value

    def var(self, mean, data):
        sum_data = 0
        n = len(data)
        for d in data:
            diff = d - mean
            sum_data += diff*diff
        return sum_data/n

    def std(self, var):
        return math.sqrt(var)

    def remove_outliers(self, data, mean):
        pass