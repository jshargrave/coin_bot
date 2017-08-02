import sqlite3
import csv


# dates used in database query should be formatted as "YYYY-MM-DD HH:MM:SS"
class HistoricalDB:
    def __init__(self):
        self.conn = sqlite3.connect('historical.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Bitcoin(id integer PRIMARY KEY, date text NOT NULL, "
                            "avg text NOT NULL, max text NOT NULL, min text NOT NULL)")

    def drop_table(self):
        self.cursor.execute("DROP TABLE Bitcoin")
        self.__init__()

    def insert_into_bitcoin(self, array_tuple):
        self.cursor.executemany("INSERT INTO Bitcoin(date, avg, max, min) VALUES (?,?,?,?)", array_tuple)
        self.conn.commit()

    def select_bitcoin(self, date_range):
        self.cursor.execute("SELECT * FROM Bitcoin WHERE date >= ? and date <= ?", date_range)
        return self.cursor.fetchall()

    def process_data_bitcoinity(self, file_path):
        read_file = open(file_path, 'r')
        csv_reader = csv.reader(read_file)

        data = []
        next(csv_reader, None)
        for row in csv_reader:
            data_line = (row[0].strip(' UTC'), row[1], row[2], row[3])
            data.append(data_line)

        read_file.close()
        self.insert_into_bitcoin(data)
