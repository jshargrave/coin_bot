from dateutil.parser import *
from datetime import *
import config as cfg
import bot_api as ba
import sqlite3
import csv
import math
import requests


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
        realtime_interval = datetime.utcnow().replace(second=0, microsecond=0) + timedelta(minutes=refresh)
        historical_interval = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)

        print("Monitoring Data...")
        while True:
            # variable used to hold the current time
            now_time = datetime.utcnow()

            # importing real time updates
            if now_time >= realtime_interval:
                self.import_bitcoin_real_time(realtime_interval)
                realtime_interval = (realtime_interval + timedelta(minutes=refresh))

            # importing historical updates
            if now_time >= historical_interval:
                self.import_bitcoin_historical(historical_interval)
                historical_interval = (historical_interval + timedelta(days=1))

    def rebuild_tables(self):
        print("Clearing all tables...", end='')
        self.cursor.execute("DROP TABLE BitcoinHistorical")
        self.cursor.execute("DROP TABLE BitcoinRealTime")
        self.cursor.execute("DROP TABLE BitcoinTrans")
        self.__init__()
        print("Completed")

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
        print("Completed: %.0f items inserted.", count)
        read_file.close()

    def import_bitcoin_historical(self, date_scope=datetime.min):
        print("Importing Historical Bitcoin...", end='')
        url = 'https://data.bitcoinity.org/export_data.csv?currency=USD&data_type=price&exchange=coinbase' \
                  '&t=l&timespan=all'
        with requests.Session() as s:
            download = s.get(url)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            next(cr, None)
            my_list = list(cr)

            data_list = []
            for row in my_list:
                if date_scope <= self.parse_time(row[0]):
                    data_list.append((row[0].strip(' UTC'), row[1]))

            s.close()
            self.insert_bitcoin_historical(data_list)
            print("Completed.")

    def import_bitcoin_real_time(self, date):
        price = ba.CoinBaseAPI(cfg.API_KEY, cfg.API_SECRET).get_price('BTC')
        self.insert_bitcoin_real_time([(date, price)])
        print(date, price)

    def parse_time(self, time_stamp):
        new_time = parse(time_stamp).replace(microsecond=0).replace(tzinfo=None)
        return new_time