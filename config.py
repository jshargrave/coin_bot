from ConfigParser import *

min = 60
hour = min * 60
day = hour * 24
month = day * 30
year = day * 365

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
MONITOR_DR = month * 3      # monitor_data(data_range(sec))
MONITOR_R = 5               # monitor_data(refresh(min))
MONITOR_LA_PER = 0.20       # monitor_data(look_ahead_per(float))
MONITOR_SED = 10            # monitor_data(stable_end_date(sec))

STABLE_T = 0.8              # is_price_stable(threshold)
STABLE_LA = min * 10        # is_price_stable(data_lookahead)

POTENTIAL_GP = 0.2          # potential_gain_strategy(gain_per)

# configurations for bot data
BD_MONITOR_R = 1            # monitor_data(refresh)

# configuration for bot data


# ----------------------------------------------------------------------------------------------------------------
