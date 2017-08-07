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

# configuration for strategies
MONITOR_DR = 86400    # monitor_data(data_range)
MONITOR_R = 5         # monitor_data(refresh)
MONITOR_LA_PER = 0.2  # monitor_data(look_ahead_per)

STABLE_DR = 60 * 60   # is_price_stable(data_look_back)
STABLE_T = 0.8        # is_price_stable(threshold)

POTENTIAL_GP = 0.2    # potential_gain_strategy(gain_per)

# configuration for bot data


# ----------------------------------------------------------------------------------------------------------------
