from bot_data import *
from coin_desk_api import *
from graph_data import *
import datetime
import datetime_funcs as df


class DataProcessing:
    def __init__(self):
        self.bot_d = BotData()
        self.cd_api = CoinDeskAPI()
        self.graph_d_rt = GraphData()
        self.graph_d_h = GraphData()

        self.build_historical_b_db()

    def build_historical_b_db(self):
        try:
            last_el = next(self.bot_d.select_last("BitcoinHistorical"))
            date_range = df.display_date(df.parse_datetime(last_el[0])), df.display_date(datetime.datetime.now())

        except StopIteration as err:
            date_range = df.btc_all_data_date_range()

        if date_range[0] != date_range[1]:
            data_generator = self.cd_api.get_btc_hist_db_data(date_range)
            self.bot_d.insert("BitcoinHistorical", data_generator)

    # ------------------------------------------- Datetime Methods ---------------------------------------------------
    '''
      Converts a string to a datetime obj
    '''
    @staticmethod
    def convert_str_to_datetime(date_obj):
        return dateutil.parser.parse(date_obj)

    '''
      Finds the difference between two dates and parameters
    '''
    @staticmethod
    def datetime_diff(datetime_obj, days=0, sec=0, microsec=0, millisec=0, min=0, hours=0, wks=0):
        return datetime_obj + datetime.timedelta(days, sec, microsec, millisec, min, hours, wks)

    # ------------------------------------- Data Calculation Methods -------------------------------------------------
    '''
      Takes a data_generator parameter that then loops through all the data and calculates the average price
    '''
    @staticmethod
    def calculate_average(data_generator):
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
    def local_max_generator(self, data_generator, t_delta=datetime.timedelta(days=1), percent_check=0.5):
        try:
            prev_data = next(data_generator)                        # stores the previous data
        except StopIteration:
            return

        oldest_date = self.convert_str_to_datetime(prev_data[0])    # oldest date
        is_increasing = False                                       # are the data prices currently increasing
        pos_max = ()                                                # data of a possible local max value

        for i in data_generator:
            current_date = self.convert_str_to_datetime(i[0])

            # check that there is t_delta data before
            if current_date > oldest_date + t_delta:
                # check if the price values are increasing
                if i[1] >= prev_data[1]:
                    is_increasing = True

                # check if the price values were increasing and are now decreasing
                if is_increasing and i[1] < prev_data[1]:
                    # if no pos_max has been found or are high max has been found
                    if pos_max == () or prev_data[1] > pos_max[1]:
                        pos_max = prev_data
                    is_increasing = False

                # found a pos_max value
                if pos_max != ():
                    # checking that a we have dates for a lookahead of t_delta
                    if current_date >= self.convert_str_to_datetime(pos_max[0]) + t_delta:
                        yield pos_max
                        pos_max = ()
            prev_data = i

    '''
      Takes a data_generator and yields the local minimums based on the t_delta parameter. 
    '''
    def local_min_generator(self, data_generator, t_delta=datetime.timedelta(days=1)):
        try:
            prev_data = next(data_generator)                        # stores the previous data
        except StopIteration:
            return

        oldest_date = self.convert_str_to_datetime(prev_data[0])    # oldest date
        is_decreasing = False                                       # are the data prices currently decreasing
        pos_min = ()                                                # data of a possible local min value

        for i in data_generator:
            current_date = self.convert_str_to_datetime(i[0])

            # check that there is t_delta data before
            if current_date > oldest_date + t_delta:
                # check if the price values are decreasing
                if i[1] <= prev_data[1]:
                    is_decreasing = True

                # check if the price values were decreasing and are now increasing
                if is_decreasing and i[1] > prev_data[1]:
                    # if no pos_min has been found or are high max has been found
                    if pos_min == () or prev_data[1] < pos_min[1]:
                        pos_min = prev_data
                    is_decreasing = False

                # found a pos_max value
                if pos_min != ():
                    # checking that a we have dates for a lookahead of t_delta
                    if current_date >= self.convert_str_to_datetime(pos_min[0]) + t_delta:
                        yield pos_min
                        pos_min = ()
            prev_data = i
