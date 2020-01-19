from configparser import *

# Time variables
minute = 60
hour = minute * 60
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

# ---------------------------------------------- bot_strategy.ph Variables ------------------------------------
# def monitor()
BEGIN_DATE_DECREMENT_SEC = month * 3        # monitor_data(data_range(sec))
MONITOR_R = minute * 5                      # monitor_data(refresh(sec))
MONITOR_LA_PER = 0.20                       # monitor_data(look_ahead_per(float))
MONITOR_SED = 10                            # monitor_data(stable_end_date(sec))

STABLE_T = 0.8                              # is_price_stable(threshold)
STABLE_LA = day                             # is_price_stable(data_lookahead)

POTENTIAL_GP = 0.2                          # potential_gain_strategy(gain_per)

# configurations for bot data
BD_MONITOR_R = 1                            # monitor_data(refresh(min))

# configuration for bot data
POI_TL = day * 5
