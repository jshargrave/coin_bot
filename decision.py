from datetime import *


# simple moving average
def sma_prediction(db, api, sec=86400):
    # date to start and end the sma calculations from
    sma_begin_date = db.parse_time(str(datetime.utcnow() - timedelta(seconds=sec)))
    sma_end_date = db.parse_time(str(datetime.utcnow()))
    date_range = (sma_begin_date, sma_end_date)

    # retrieving all relevant data for sma calculation
    sma_select = db.select_bitcoin_date(date_range)

    # retrieving all data in database
    all_select = db.select_bitcoin_all()



