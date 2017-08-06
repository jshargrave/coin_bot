from historical import *
from coinbase_api import *
from decision import *

from ConfigParser import *
from signal import *


# --------------------------------------------- Config File Settings --------------------------------------------
config = RawConfigParser()
config.read("config.cfg")

# parse config file
API_KEY = config.get('API', 'API Key')
API_SECRET = config.get('API', 'API Secret')

# get data information
FILE_PATH = config.get('Data', 'file')


# ---------------------------------------------- Standard Global Variables --------------------------------------
# historical
REBUILD_DB = False

DB = HistoricalDB()
API_LIST = [CoinBaseAPI(API_KEY, API_SECRET)]

# decision
# coinbase_api



