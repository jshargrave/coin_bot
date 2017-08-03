from coinbase_api import *
from decision import *
from historical import *

# constants used for quick time calculations
min = 60
hour = min * 60
day = hour * 24


def run_bot(api_key, api_secret):
    sma_prediction(HistoricalDB(), CoinBaseAPI(api_key, api_secret), day * 30)


def import_data(file_path, rebuild):
    database = HistoricalDB()

    if rebuild.lower() == "true":
        database.drop_table()

    database.process_data_bitcoinity(file_path)
