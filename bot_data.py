from datetime import *
import sqlite3


# dates used in database query should be formatted as "YYYY-MM-DD HH:MM:SS"
class BotData:
    def __init__(self, name="BotData.db"):
        self.name = name
        self.conn = sqlite3.connect(name)
        self.cursor = self.conn.cursor()
        self.build_all_tables()

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
                  "  UNIQUE(date)" \
                  ");"
        self.execute_sql_command(sql_cmd)

        sql_cmd = "CREATE TABLE IF NOT EXISTS BitcoinRealTime (" \
                  "  id integer PRIMARY KEY, " \
                  "  date text NOT NULL, " \
                  "  price real NOT NULL," \
                  "  UNIQUE(date)" \
                  ");"
        self.execute_sql_command(sql_cmd)

    def drop_all_tables(self):
        self.drop_table("BitcoinHistorical")
        self.drop_table("BitcoinRealTime")

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

    # This function is used as a generator to yield select results.  Run this function after a select exicutes to yield
    # the results.  The amount parameter specifies how many rows to select at a time.
    def select_generator(self, amount=1000):
        while True:
            rows = self.cursor.fetchmany(amount)
            if not rows:
                break
            for row in rows:
                yield row
