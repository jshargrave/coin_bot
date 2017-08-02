from communications import *
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read("config.cfg")

# parse config file
api_key = config.get('API', 'API Key')
api_secret = config.get('API', 'API Secret')

# get data information
file_path = config.get('Data', 'file')
rebuild = config.get('Data', 'rebuild database')


import_data(file_path, rebuild)
run_bot(api_key, api_secret)