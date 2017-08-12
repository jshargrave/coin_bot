import config as cfg
import math


class BotAnalysis:
    def find_poi(self, x, y, mean, s, threshold=1):
        n = 0
        if len(x) == len(y):
            n = len(x)
        else:
            print("Error: len(x) != len(y)")


        for i in range(n):
            z = (y[i] - mean)/s

            if z > threshold:
                pass
            elif z < threshold:
                pass


    '''
    def find_poi(self, x, y, local_max, local_min, abs_max, abs_min, mean, std, time_limit=cfg.POI_TL):
        n = len(x)
        value_increase = False
        value_decrease = False
        max_index = []
        min_index = []

        for i in range(n):
            if y[i] > abs_max[1]:
                abs_max = (x[i], y[i])
            if y[i] < abs_min[1]:
                abs_min = (x[i], y[i])
            if i == 0:
                continue
            if i == n - 1:
                continue

            # values are increasing
            if y[i - 1] < y[i]:
                # potential dip found
                if value_decrease:
                    value_decrease = False
                    data_range = self.decrement_date(self.parse_time(str(x[i - 1])), s=time_limit)
                    add_index = True
                    # adding dip logic
                    if len(min_index) > 0:
                        if x[min_index[0]] >= data_range:
                            if y[i - 1] >= y[min_index[0]]:
                                add_index = False
                            elif y[i - 1] < y[min_index[0]]:
                                del min_index[0]

                    if add_index and y[i - 1] < mean - std:
                        min_index.insert(0, i - 1)

                value_increase = True

            # values are decreasing
            if y[i - 1] > y[i]:
                # potential peak found
                if value_increase:
                    value_increase = False
                    data_range = self.decrement_date(self.parse_time(str(x[i - 1])), s=time_limit)
                    add_index = True
                    # adding peak logic
                    if len(max_index) > 0:
                        if x[max_index[0]] >= data_range:
                            if y[i - 1] <= y[max_index[0]]:
                                add_index = False
                            if y[i - 1] > y[max_index[0]]:
                                del max_index[0]

                    if add_index and y[i - 1] > mean + std:
                        max_index.insert(0, i - 1)

                value_decrease = True

        # local_min and local_max are empty (first time running poi), therefore remove the last elm and append
        if local_min != ([], []) and local_max != ([], []):
            del local_max[0][-1]
            del local_max[1][-1]
            del local_min[0][-1]
            del local_min[1][-1]

        for max_i in reversed(max_index):
            local_max[0].append(x[max_i])
            local_max[1].append(y[max_i])

        for min_i in reversed(min_index):
            local_min[0].append(x[min_i])
            local_min[1].append(y[min_i])

        if len(max_index) == 0 and len(min_index) == 0:
            index = (0, 0)
        elif len(max_index) == 0:
            index = (0, min_index[0])
        elif len(min_index) == 0:
            index = (max_index[0], 0)
        else:
            index = (max_index[0], min_index[0])

        return local_max, local_min, abs_max, abs_min, index
    '''


    def var(self, mean, data):
        sum_data = 0
        n = len(data)
        for d in data:
            diff = d - mean
            sum_data += diff*diff
        return sum_data/n

    def std(self, var):
        return math.sqrt(var)