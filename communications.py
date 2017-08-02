from coinbase_api import *
from decision import *
from historical import *


def run_bot(api_key, api_secret):
    api = CoinBaseAPI(api_key, api_secret)


def import_data(file_path, rebuild):
    database = HistoricalDB()

    if rebuild.lower() == "true":
        database.drop_table()

    database.process_data_bitcoinity(file_path)