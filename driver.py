from communications import *
import ConfigParser


config = ConfigParser.RawConfigParser()
config.read("config.cfg")

# parse config file
api_key = config.get('API', 'API Key')
api_secret = config.get('API', 'API Secret')


run_bot(api_key, api_secret)