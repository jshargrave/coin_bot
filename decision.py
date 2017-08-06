import config as cfg
from datetime import *
import matplotlib.pyplot as plt
import numpy


def graph_data():
    sma_begin_date = cfg.DB.parse_time(str(datetime.utcnow() - timedelta(seconds=7776000)))
    sma_end_date = cfg.DB.parse_time(str(datetime.utcnow()))
    date_range = (sma_begin_date, sma_end_date)

    select = cfg.DB.select_bitcoin_date(date_range)
    #select = cfg.DB.select_bitcoin_all()

    all_y_avg = []
    all_y_max = []
    all_y_min = []
    all_x = []

    for row in select:
        values = (cfg.DB.parse_time(row[1]), float(row[2]), float(row[3]), float(row[4]))
        all_y_avg.append(values[1])
        all_y_max.append(values[2])
        all_y_min.append(values[3])
        all_x.append(values[0])

    print(len(select))
    local_maximums = calculate_local_max(all_x, all_y_avg, 10)
    local_minimums = calculate_local_min(all_x, all_y_avg, 10)
    absolute_max = find_absolute_max(all_x, all_y_avg)
    absolute_min = find_absolute_min(all_x, all_y_avg)

    print(absolute_max)
    print(absolute_min)




    # plot avg, max, min
    plt.plot(all_x, all_y_avg, linewidth=1)
    #plt.plot(all_x, all_y_max)
    #plt.plot(all_x, all_y_min)

    # plot max and min avg
    plt.plot(local_maximums[0], local_maximums[1], 'ro')
    plt.plot(local_minimums[0], local_minimums[1], 'bs')

    # plot absolute max and min
    plt.plot([absolute_max[0]], [absolute_max[1]], 'g^')
    plt.plot([absolute_min[0]], [absolute_min[1]], 'g^')


    plt.gcf().autofmt_xdate()
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.show()


def calculate_local_max(x, y, look_ahead):
    n = len(y)
    local_max_x = []
    local_max_y = []

    # note dont index anything less then 0 and greater than n - 1
    i = 0
    while i < n:
        # value to inspect
        value = y[i]
        l_condition, r_condition = True, True

        # check left side
        l_count = 0
        while l_count < look_ahead:
            index = i - l_count - 1
            if index < 0:
                break
            if y[index] > value:
                l_condition = False
                break
            l_count += 1

        # check right side
        r_count = 0
        while r_count < look_ahead:
            index = i + r_count + 1
            if index > n - 1:
                break
            if y[index] > value:
                r_condition = False
                break
            r_count += 1

        # checking if local maximum conditions were met
        if l_condition and r_condition:
            local_max_x.append(x[i])
            local_max_y.append(y[i])

        i += 1

    return local_max_x, local_max_y


def calculate_local_min(x, y, look_ahead):
    n = len(y)
    local_min_x = []
    local_min_y = []

    # note dont index anything less then 0 and greater than n - 1
    i = 0
    while i < n:
        # value to inspect
        value = y[i]
        l_condition, r_condition = True, True

        # check left side
        l_count = 0
        while l_count < look_ahead:
            index = i - l_count - 1
            if index < 0:
                break
            if y[index] < value:
                l_condition = False
                break
            l_count += 1

        # check right side
        r_count = 0
        while r_count < look_ahead:
            index = i + r_count + 1
            if index > n - 1:
                break
            if y[index] < value:
                r_condition = False
                break
            r_count += 1

        # checking if local maximum conditions were met
        if l_condition and r_condition:
            local_min_x.append(x[i])
            local_min_y.append(y[i])

        i += 1

    return local_min_x, local_min_y


def find_absolute_max(x, y):
    n = len(y)
    max_value = y[0]
    max_date = datetime

    for i in range(n):
        if y[i] > max_value:
            max_value = y[i]
            max_date = x[i]

    return max_date, max_value


def find_absolute_min(x, y):
    n = len(y)
    min_value = y[0]
    min_date = datetime

    for i in range(n):
        if y[i] < min_value:
            min_value = y[i]
            min_date = x[i]

    return min_date, min_value

'''
from datetime import *
from sklearn import linear_model


# simple moving average

def sma_prediction(db, api_list, sec=86400):
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
        values = (float(db.parse_time(row[1]).toordinal()), float(row[2]), float(row[3]), float(row[4]))
        sma_x_avg.append(values[1])
        sma_x_max.append(values[2])
        sma_x_min.append(values[3])
        sma_y.append(values[0])

    for row in all_select:
        values = (float(db.parse_time(row[1]).toordinal()), float(row[2]), float(row[3]), float(row[4]))
        all_x_avg.append(values[1])
        all_x_max.append(values[2])
        all_x_min.append(values[3])
        all_y.append(values[0])

    linear_regression(sma_y, sma_x_avg)
    linear_regression(sma_y, sma_x_max)
    linear_regression(sma_y, sma_x_min)
    linear_regression(all_y, all_x_avg)
    linear_regression(all_y, all_x_max)
    linear_regression(all_y, all_x_min)

def linear_regression(x, y):
    regr = linear_model.LinearRegression()
    # split the values into two series instead a list of tuples
    max_x = max(x)
    min_x = min(x)
    # split the values in train and data.
    train_data_X = map(lambda x: [x], list(x[:-20]))
    train_data_Y = list(y[:-20])
    test_data_X = map(lambda x: [x], list(x[-20:]))
    test_data_Y = list(y[-20:])
    # feed the linear regression with the train data to obtain a model.
    regr.fit(train_data_X, train_data_Y)
    # check that the coeffients are the expected ones.
    m = regr.coef_[0]
    b = regr.intercept_
    print(' y = {0} * x + {1}'.format(m, b))

'''