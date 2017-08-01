from coinbase_api import *
from decision import *
from historical import *


def run_bot(api_key, api_secret):
    API = CoinBaseAPI(api_key, api_secret)
    print(API.get_spot_price())