from ConfigParser import *


# --------------------------------------------- Config File Settings --------------------------------------------
config = RawConfigParser()
config.read("config.cfg")

# parse config file
API_KEY = config.get('CoinBase API', 'API Key')
API_SECRET = config.get('CoinBase API', 'API Secret')

# get data information
FILE_PATH_BITCOINITY = config.get('Data', 'bitcoinity file')
FILE_PATH_KAGGLE = config.get('Data', 'kaggle file')


# ----------------------------------------------------------------------------------------------------------------
