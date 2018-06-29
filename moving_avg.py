"""
    Desc:  This file deals with calculation for the moving average.  The class is capable of linking to a database
"""

import datetime
import datetime_funcs


class MovingAverage:
    def __init__(self, data_func, time_delta_lookback, time_delta_interval):
        # Function to retrieve the data
        self.data_func = data_func

        # This is the amount of time to calculate the moving average over
        self.time_delta_lookback = time_delta_lookback

        # Time delta interval to calculate the averages across
        self.time_delta_interval = time_delta_interval

    def get_data(self):
        return self.data_func(self.get_date_range())

    def get_date_range(self):
        return [datetime.datetime.now() - self.time_delta_lookback, datetime.datetime.now()]

    def calculate_simple_moving_average(self):
        # Set starting values
        avg = 0
        count = 0
        datetime_interval = None
        datetime_list = []

        # Setting up generators, this throws away the first data point
        data_gen = self.get_data()
        start_date = datetime_funcs.parse_datetime(next(data_gen)[1])
        datetime_gen = datetime_funcs.increment_datetime_generator(start_date, self.time_delta_interval)

        # Loop through data
        for i in data_gen:
            # Add to variables
            avg += i[2]
            count += 1
            current_datetime = datetime_funcs.parse_datetime(i[1])
            datetime_list.append(current_datetime)

            # Check if datetime_interval is None
            if not datetime_interval:
                # Set next datetime_interval
                datetime_interval = next(datetime_gen)

                # Do this so that datetime_interval does not fall behind current_datetime
                if current_datetime >= datetime_interval:
                    datetime_gen.close()
                    datetime_gen = datetime_funcs.increment_datetime_generator(current_datetime, self.time_delta_interval)
                    datetime_interval = current_datetime

            # Check if datetime_interval was passed
            if current_datetime >= datetime_interval:
                avg_datetime = datetime_funcs.average_datetime(datetime_list)
                yield [datetime_funcs.display_datetime(avg_datetime), round(avg / count, 2)]

                # Reset variables
                avg = 0
                count = 0
                datetime_interval = None
                datetime_list = []


    def calculate_exponential_moving_average(self): pass




