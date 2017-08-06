import config as cfg
from dateutil.parser import *
import sqlite3
import csv
from datetime import *
import time
import sys


run = True

# dates used in database query should be formatted as "YYYY-MM-DD HH:MM:SS"
class HistoricalDB:
    def __init__(self):
        self.conn = sqlite3.connect('historical.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Bitcoin(id integer PRIMARY KEY, date text NOT NULL, "
                            "avg text NOT NULL, max text NOT NULL, min text NOT NULL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS ShortTerm(id integer PRIMARY KEY, date text NOT NULL, "
                            "price text NOT NULL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Transactions(id integer PRIMARY KEY, date text NOT NULL, "
                            "amount text NOT NULL, price text NOT NULL)")

    def drop_table(self):
        self.cursor.execute("DROP TABLE Bitcoin")
        self.__init__()

    def insert_into_bitcoin(self, array_tuple):
        self.cursor.executemany("INSERT INTO Bitcoin(date, avg, max, min) VALUES (?,?,?,?)", array_tuple)
        self.conn.commit()

    def insert_into_short_term(self, array_tuple):
        self.cursor.executemany("INSERT INTO shortTerm(date, price) VALUES (?,?)", array_tuple)
        self.conn.commit()

    def insert_into_transactions(self, array_tuple):
        self.cursor.executemany("INSERT INTO Transactions(date, amount, price) VALUES (?,?,?)", array_tuple)
        self.conn.commit()

    def select_bitcoin_date(self, date_range):
        self.cursor.execute("SELECT * FROM Bitcoin WHERE date >= ? and date <= ?", date_range)
        return self.cursor.fetchall()

    def select_bitcoin_all(self):
        self.cursor.execute("SELECT * FROM Bitcoin")
        return self.cursor.fetchall()

    def process_data_bitcoinity(self, file_path):
        read_file = open(file_path, 'r')
        csv_reader = csv.reader(read_file)

        data = []
        next(csv_reader, None)
        for row in csv_reader:
            data_line = (self.parse_time(row[0]), row[1], row[2], row[3])
            data.append(data_line)

        read_file.close()
        self.insert_into_bitcoin(data)

    def parse_time(self, time_stamp):
        new_time = parse(time_stamp).replace(microsecond=0).replace(tzinfo=None)
        return new_time

    def retrieve_data(self, min):
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
                for api in cfg.API_LIST:
                    price = api.get_price().amount
                    insert_array.append((time_stamp, price))

                # inserting values into database
                self.insert_into_short_term(insert_array)
                sys.stdout.write('.')
                sys.stdout.flush()

            # updating interval_time
            if interval_time <= now_time:
                interval_time = now_time + timedelta(minutes=min)