import sqlite3
import datetime_funcs


# dates used in database query should be formatted as "YYYY-MM-DD HH:MM:SS"
class BotData:
    def __init__(self, data_func_dict, name="data/BotData.db"):
        self.name = name
        self.conn = sqlite3.connect(name)
        self.cursor = self.conn.cursor()
        self.data_func_dict = data_func_dict

        # Rebuilding the database
        self.rebuild_tables()
        self.insert_all_data()

    # Opens a connection to database $name
    def open_database(self):
        self.conn = sqlite3.connect(self.name)
        self.cursor = self.conn.cursor()

    # Closes current database connection
    def close_database(self):
        self.conn.commit()
        self.conn.close()

    # Executes a sql command passed by parameter on the current connected database
    def execute_sql_command(self, sql_cmd):
        self.cursor.execute(sql_cmd)

    def drop_table(self, table):
        self.execute_sql_command("DROP TABLE "+table+";")

    def build_all_tables(self):
        sql_cmd = "CREATE TABLE IF NOT EXISTS BitcoinHistorical (" \
                  "  id integer PRIMARY KEY, " \
                  "  date text NOT NULL, " \
                  "  price real NOT NULL," \
                  "  UNIQUE(id, date)" \
                  ");"
        self.execute_sql_command(sql_cmd)

        sql_cmd = "CREATE TABLE IF NOT EXISTS BitcoinRealTime (" \
                  "  id integer PRIMARY KEY, " \
                  "  date text NOT NULL, " \
                  "  price real NOT NULL," \
                  "  UNIQUE(id, date)" \
                  ");"
        self.execute_sql_command(sql_cmd)

    def drop_all_tables(self):
        # Select all tabels
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

        # Loop through result
        for i in self.select_generator():
            self.drop_table(i[0])

    def rebuild_tables(self):
        self.drop_all_tables()
        self.build_all_tables()

    # ----------------------------------------------- Insert Commands ------------------------------------------
    def insert_bh(self, array_tuple):
        self.cursor.executemany("INSERT INTO BitcoinHistorical (date, price) "
                                "VALUES (?,?);", array_tuple)
        self.conn.commit()

    def insert_brt(self, array_tuple):
        self.cursor.executemany("INSERT INTO BitcoinRealTime(date, price) "
                                "VALUES (?,?);", array_tuple)
        self.conn.commit()

    # ------------------------------------------------ Delete Commands -----------------------------------------
    def delete_where_bh(self, condition):
        sql_cmd = "DELETE FROM BitcoinHistorical " \
                  "WHERE "+ condition + ";"
        self.execute_sql_command(sql_cmd)
        self.conn.commit()

    def delete_where_brt(self, condition):
        sql_cmd = "DELETE FROM BitcoinRealTime " \
                  "WHERE " + condition + ";"
        self.execute_sql_command(sql_cmd)
        self.conn.commit()

    # ------------------------------------------- Select Commands ------------------------------------------------
    def select_bh_range(self, date_range):
        self.cursor.execute("SELECT * FROM BitcoinHistorical "
                            "WHERE date >= ? AND date <= ? "
                            "ORDER BY date ASC;", date_range)
        for i in self.select_generator():
            yield i

    def select_bh_all(self):
        self.cursor.execute("SELECT * FROM BitcoinHistorical "
                            "ORDER BY date ASC;")
        for i in self.select_generator():
            yield i

    def select_brt_range(self, date_range):
        self.cursor.execute("SELECT * FROM BitcoinRealTime "
                            "WHERE date >= ? AND date <= ? "
                            "ORDER BY date ASC;", date_range)
        for i in self.select_generator():
            yield i

    def select_brt_all(self):
        self.cursor.execute("SELECT * FROM BitcoinRealTime "
                            "ORDER BY date ASC;")
        for i in self.select_generator():
            yield i

    # ------------------------------------------- Misc Functions -------------------------------------------

    # This function is used as a generator to yield select results.  This function is automatically called after each
    # select command on the database is executed.  The amount parameter specifies how many rows to select at a time.
    def select_generator(self, amount=1000):
        while True:
            rows = self.cursor.fetchmany(amount)
            if not rows:
                break
            for row in rows:
                yield row

    def insert_all_data(self):
        # Insert historical data
        if 'BTC_Historical' in self.data_func_dict.keys():
            date_range = datetime_funcs.btc_all_data_date_range()
            data = self.data_func_dict['BTC_Historical'](date_range)
            self.insert_bh(data)

        # Insert real time data
        if 'BTC_Real_Time' in self.data_func_dict.keys():
            data = self.data_func_dict['BTC_Real_Time']()
            self.insert_brt(data)

