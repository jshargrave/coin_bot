import bot_data as bd
bd.BotData().rebuild_tables()
bd.BotData().import_bitcoin_historical()
bd.BotData().monitor_data()