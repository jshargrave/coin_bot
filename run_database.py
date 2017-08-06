import bot_data as bd
bd.BotData().rebuild_tables()
#cfg.DB.process_data_kaggle(cfg.FILE_PATH_KAGGLE)
bd.BotData().retrieve_data(1)
