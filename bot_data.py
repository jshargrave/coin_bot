import sqlite3
import datetime_funcs


# dates used in database query should be formatted as "YYYY-MM-DD HH:MM:SS"
class BotData:
    def __init__(self, name="data/BotData.db"):
        self.table_meta = {
            "BitcoinHistorical": {
                "Name": "BitcoinHistorical",
                "CreateCmd": "CREATE TABLE IF NOT EXISTS BitcoinHistorical ("
                             "  date text NOT NULL PRIMARY KEY, "
                             "  price real NOT NULL,"
                             "  UNIQUE(date)"
                             ");",
                "InsertCmd": "INSERT or REPLACE INTO BitcoinHistorical (date, price) "
                             "VALUES (?,?);",
                "SelectWhereDateCmd": "SELECT * FROM BitcoinHistorical "
                                      "WHERE date >= ? AND date <= ? "
                                      "ORDER BY date ASC;",
                "SelectAllCmd": "SELECT * FROM BitcoinHistorical "
                                "ORDER BY date ASC;",
                "SelectNewCmd": "SELECT * "
                                "FROM "
                                "("
                                "   SELECT * FROM BitcoinHistorical "
                                "   ORDER BY date DESC "
                                "   LIMIT (?) "
                                ")"
                                "ORDER BY date ASC;",
                "SelectLastCmd": "SELECT * FROM BitcoinRealTime "
                                 "ORDER BY date DESC "
                                 "LIMIT 1 ",
                "NewCount": "0",
            },
            "BitcoinRealTime": {
                "Name": "BitcoinRealTime",
                "CreateCmd": "CREATE TABLE IF NOT EXISTS BitcoinRealTime ("
                             "  date text NOT NULL PRIMARY KEY, "
                             "  price real NOT NULL,"
                             "  UNIQUE(date)"
                             ");",
                "InsertCmd": "INSERT or REPLACE INTO BitcoinRealTime (date, price) "
                             "VALUES (?,?);",
                "SelectWhereDateCmd": "SELECT * FROM BitcoinRealTime "
                                      "WHERE date >= ? AND date <= ? "
                                      "ORDER BY date ASC;",
                "SelectAllCmd": "SELECT * FROM BitcoinRealTime "
                                "ORDER BY date ASC;",
                "SelectNewCmd": "SELECT * "
                                "FROM "
                                "("
                                "   SELECT * FROM BitcoinRealTime "
                                "   ORDER BY date DESC "
                                "   LIMIT (?) "
                                ")"
                                "ORDER BY date ASC;",
                "SelectLastCmd": "SELECT * FROM BitcoinRealTime "
                                 "ORDER BY date DESC "
                                 "LIMIT 1 ",
                "NewCount": "0"
            }
        }

        self.name = name
        self.conn = sqlite3.connect(name)
        self.cursor = self.conn.cursor()

        # Rebuilding the database
        #self.rebuild_tables()
        self.build_all_tables()

    # Opens a connection to database $name
    def open_database(self):
        self.conn = sqlite3.connect(self.name)
        self.cursor = self.conn.cursor()

    # Closes current database connection
    def close_database(self):
        self.conn.commit()
        self.conn.close()

    def drop_table(self, table):
        self.cursor.execute("DROP TABLE "+table+";")

    def build_all_tables(self):
        for key, item in self.table_meta.items():
            sql_cmd = item["CreateCmd"]
            self.cursor.execute(sql_cmd)

    def drop_all_tables(self):
        # Select all tables
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

        # Loop through result
        for i in self.select_generator():
            self.drop_table(i[0])

    def rebuild_tables(self):
        self.drop_all_tables()
        self.build_all_tables()

    # ----------------------------------------------- Insert Commands ------------------------------------------
    def insert(self, table, array_tuple):
        if table in self.table_meta.keys():
            sql_cmd = self.table_meta[table]["InsertCmd"]
            self.cursor.executemany(sql_cmd, array_tuple)
            self.conn.commit()

            # Update new element
            self.table_meta[table]["NewCount"] = str(int(self.table_meta[table]["NewCount"]) + len(array_tuple))

    # ------------------------------------------- Select Commands ------------------------------------------------
    def select(self, table, date_range=tuple()):
        if table in self.table_meta.keys():
            if date_range:
                sql_cmd = self.table_meta[table]["SelectAllCmd"]
                self.cursor.execute(sql_cmd)
            else:
                sql_cmd = self.table_meta[table]["SelectWhereDateCmd"]
                self.cursor.execute(sql_cmd, date_range)

            for i in self.select_generator():
                yield i

    def select_new(self, table):
        if table in self.table_meta.keys():
            if self.table_meta[table]["NewCount"]:
                sql_cmd = self.table_meta[table]["SelectNewCmd"]
                new_count = (self.table_meta[table]["NewCount"], )
                self.cursor.execute(sql_cmd, new_count)

                # Clear NewCount
                self.table_meta[table]["NewCount"] = "0"

                for i in self.select_generator():
                    yield i

    def select_last(self, table):
        if table in self.table_meta.keys():
            sql_cmd = self.table_meta[table]["SelectLastCmd"]
            self.cursor.execute(sql_cmd)

            for i in self.select_generator():
                yield i

    def select_all(self, table):
        if table in self.table_meta.keys():
            sql_cmd = self.table_meta[table]["SelectAllCmd"]
            self.cursor.execute(sql_cmd)

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
