import matplotlib.pyplot as plt
import bot_data as bd
from datetime import *



class GraphChart:
    def real_time_graph(self, data_look_back, refresh, look_ahead_per):
        begin_date = bd.BotData().parse_time(str(datetime.utcnow() - timedelta(seconds=data_look_back)))
        date_range = (begin_date, bd.BotData().parse_time(str(datetime.utcnow())))

        plt.ion()
        plt.xlabel("Date")
        plt.ylabel("Price")

        all_y = []
        all_x = []

        interval_time = datetime.utcnow().replace(second=0, microsecond=0)
        while True:
            # variable used to hold the current time
            now_time = datetime.utcnow().replace(second=0, microsecond=0)

            # checking if interval has completed
            if interval_time == now_time:
                select = bd.BotData().select_bitcoin_real_time(date_range)

                for row in select:
                    values = (bd.BotData().parse_time(row[1]), float(row[2]))
                    all_y.append(values[1])
                    all_x.append(values[0])

                n = len(all_x)
                if len(all_x) != 0 and len(all_y) != 0 and len(all_x) == len(all_y):
                    local_maximums = bd.BotData().calculate_local_max(all_x, all_y, int(n * look_ahead_per) + 1)
                    local_minimums = bd.BotData().calculate_local_min(all_x, all_y, int(n * look_ahead_per) + 1)
                    absolute_max = bd.BotData().find_absolute_max(all_x, all_y)
                    absolute_min = bd.BotData().find_absolute_min(all_x, all_y)

                    # clear entire figure
                    plt.clf()

                    # plot avg, max, min
                    plt.plot(all_x, all_y)

                    # plot max and min avg
                    plt.plot(local_maximums[0], local_maximums[1], 'ro')
                    plt.plot(local_minimums[0], local_minimums[1], 'bs')

                    # label absolute max and min
                    plt.annotate(
                        "Absolute Max",
                        xy=absolute_max, xytext=(-20, 20),
                        textcoords='offset points', ha='right', va='bottom',
                        bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

                    plt.annotate(
                        "Absolute Min",
                        xy=absolute_min, xytext=(-20, 20),
                        textcoords='offset points', ha='right', va='bottom',
                        bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

                    plt.gcf().autofmt_xdate()
                    plt.pause(0.05)

            # updating interval_time
            if interval_time <= now_time:
                interval_time = now_time + timedelta(minutes=refresh)
                date_range = (date_range[1], interval_time)
