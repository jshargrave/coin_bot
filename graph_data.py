import matplotlib.pyplot as plt
import bot_data as bd


class GraphChart:
    def graph_data(self, x, y, local_maximums, local_minimums, absolute_max, absolute_min):
        mean = sum(y) / len(y)
        std = bd.BotData().std(bd.BotData().var(mean, y))

        plt.ion()
        plt.xlabel("Date")
        plt.ylabel("Price")

        # clear entire figure
        plt.clf()

        # plot avg, max, min
        plt.plot(x, y)

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
            xy=absolute_min, xytext=(-40, 0),
            textcoords='offset points', ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

        # draw mean, mean + std, and mean - std
        plt.axhline(mean, color='r')
        plt.axhline(mean + std, color='b')
        plt.axhline(mean - std, color='b')
        plt.gcf().autofmt_xdate()

        plt.pause(0.05)
