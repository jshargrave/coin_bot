from bot_data import *
from coin_desk_api import *
from graph_data import *
import datetime


class DataProcessing:
    def __init__(self):
        self.bot_d = BotData()
        self.cd_api = CoinDeskAPI()
        self.graph_d = GraphData()

    # ----------------------------------------- Insert Methods --------------------------------------------------------
    '''
      Inserts btc realtime price into database real time table.
    '''
    def insert_btc_rt_into_db(self):
        self.bot_d.insert_brt([self.cd_api.get_btc_price()])

    '''
      Inserts btc yesterdays historical price into the database historical table.
    '''
    def insert_btc_hist_into_db_yest(self):
        self.bot_d.insert_bh([self.cd_api.get_btc_yesterdays_price()])

    '''
      Inserts btc historical data into database historical table based on the data range.
    '''
    def insert_btc_hist_into_db(self, data_range):
        self.bot_d.insert_bh(self.cd_api.get_btc_hist_db_data(data_range))

    # ------------------------------------------ Select Methods ------------------------------------------------------
    '''
      Returns a generator from the btc historical table over the data_range
    '''
    def select_btc_hist_range(self, data_range):
        return self.bot_d.select_bh_range(data_range)

    '''
      Returns a generator from the btc historical table over all data
    '''
    def select_btc_hist_all(self):
        return self.bot_d.select_bh_all()

    '''
      Returns a generator from the btc real-time table over the data_range
    '''
    def select_btc_rt_range(self, data_range):
        return self.bot_d.select_brt_range(data_range)

    '''
      Returns a generator from the btc real_time table over all data
    '''
    def select_btc_rt_all(self):
        return self.bot_d.select_brt_all()

    # ---------------------------------------- Graphing Methods ------------------------------------------------------
    '''
      Passes a generator function to the graphing function in the graph_data file.
    '''
    def graph_data_bh_range(self, data_range):
        self.graph_d.graph_data(self.bot_d.select_bh_range(data_range))

    def graph_data_bh_range_max(self, data_range, t_delta):
        select_generator = self.bot_d.select_bh_range(data_range)
        self.graph_d.graph_max(self.local_max_generator(select_generator, t_delta))

    def graph_data_bh_range_min(self, data_range, t_delta):
        select_generator = self.bot_d.select_bh_range(data_range)
        self.graph_d.graph_min(self.local_min_generator(select_generator, t_delta))

    # ------------------------------------------- Datetime Methods ---------------------------------------------------
    '''
      Converts a string to a datetime obj
    '''
    def convert_str_to_datetime(self, date_obj):
        return dateutil.parser.parse(date_obj)

    '''
      Finds the difference between two dates and parameters
    '''
    def datetime_diff(self, datetime_obj, days=0, sec=0, microsec=0, millisec=0, min=0, hours=0, wks=0):
        return datetime_obj + datetime.timedelta(days, sec, microsec, millisec, min, hours, wks)

    # ------------------------------------- Data Calculation Methods -------------------------------------------------
    '''
      Takes a data_generator parameter that then loops through all the data and calculates the average price
    '''
    def calculate_average(self, data_generator):
        sum = 0
        count = 0
        for i in data_generator:
            sum += i[2]
            count += 1
        if count == 0:
            return 0
        return sum/count

    '''
      Takes a data_generator and yields the local maximums based on the t_delta parameter.  
    '''
    def local_max_generator(self, data_generator, t_delta=datetime.timedelta(days=1)):
        prev_data = next(data_generator)                            # stores the previous data
        oldest_date = self.convert_str_to_datetime(prev_data[1])    # oldest date
        is_increasing = False                                       # are the data prices currently increasing
        pos_max = ()                                                # data of a possible local max value

        for i in data_generator:
            current_date = self.convert_str_to_datetime(i[1])

            # check that there is t_delta data before
            if current_date > oldest_date + t_delta:
                # check if the price values are increasing
                if i[2] >= prev_data[2]:
                    is_increasing = True

                # check if the price values were increasing and are now decreasing
                if is_increasing and i[2] < prev_data[2]:
                    # if no pos_max has been found or are high max has been found
                    if pos_max == () or prev_data[2] > pos_max[2]:
                        pos_max = prev_data
                    is_increasing = False

                # found a pos_max value
                if pos_max != ():
                    # checking that a we have dates for a lookahead of t_delta
                    if current_date >= self.convert_str_to_datetime(pos_max[1]) + t_delta:
                        yield pos_max
                        pos_max = ()
            prev_data = i

    '''
      Takes a data_generator and yields the local minimums based on the t_delta parameter. 
    '''
    def local_min_generator(self, data_generator, t_delta):
        prev_data = next(data_generator)                            # stores the previous data
        oldest_date = self.convert_str_to_datetime(prev_data[1])    # oldest date
        is_decreasing = False                                       # are the data prices currently decreasing
        pos_min = ()                                                # data of a possible local min value

        for i in data_generator:
            current_date = self.convert_str_to_datetime(i[1])

            # check that there is t_delta data before
            if current_date > oldest_date + t_delta:
                # check if the price values are decreasing
                if i[2] <= prev_data[2]:
                    is_decreasing = True

                # check if the price values were decreasing and are now increasing
                if is_decreasing and i[2] > prev_data[2]:
                    # if no pos_min has been found or are high max has been found
                    if pos_min == () or prev_data[2] < pos_min[2]:
                        pos_min = prev_data
                    is_decreasing = False

                # found a pos_max value
                if pos_min != ():
                    # checking that a we have dates for a lookahead of t_delta
                    if current_date >= self.convert_str_to_datetime(pos_min[1]) + t_delta:
                        yield pos_min
                        pos_min = ()
            prev_data = i
