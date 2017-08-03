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

    # lists used for linear regression
    sma_x_avg = []
    sma_x_max = []
    sma_x_min = []
    sma_y = []

    all_x_avg = []
    all_x_max = []
    all_x_min = []
    all_y = []

    # populating lists
    for row in sma_select:
        sma_x_avg.append(row[2])
        sma_x_max.append(row[3])
        sma_x_min.append(row[4])
        sma_y.append(db.parse_time(row[1]).toordinal())

    for row in all_select:
        all_x_avg.append(row[2])
        all_x_max.append(row[3])
        all_x_min.append(row[4])
        all_y.append(db.parse_time(row[1]).toordinal())

def linear_regression():

