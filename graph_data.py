import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import dateutil.parser


class GraphData:
    def __init__(self):
        self.fig1, (self.ax1) = plt.subplots(1)

        # Returns a tuple of line objects, thus the comma
        self.line1, self.max_line, self.min_line = self.ax1.plot([], [], 'r-', [], [], 'g|', [], [], 'b|')
        self.line1._linewidth = 0.5
        self.max_line._linewidth = 2
        self.min_line._linewidth = 2

        self.fig1.autofmt_xdate()
        self.xfmt = mdates.DateFormatter("%Y-%m-%d")
        self.ax1.xaxis.set_major_formatter(self.xfmt)

    def update_line(self, new_data):
        # appending new data to x and y lists
        x, y = new_data
        self.line1.set_xdata(np.append(self.line1.get_xdata(), x))
        self.line1.set_ydata(np.append(self.line1.get_ydata(), y))

    def update_max(self, new_data):
        # appending new data to x and y lists
        x, y = new_data
        self.max_line.set_xdata(np.append(self.max_line.get_xdata(), x))
        self.max_line.set_ydata(np.append(self.max_line.get_ydata(), y))

    def update_min(self, new_data):
        # appending new data to x and y lists
        x, y = new_data
        self.min_line.set_xdata(np.append(self.min_line.get_xdata(), x))
        self.min_line.set_ydata(np.append(self.min_line.get_ydata(), y))

    def graph_data(self, data_generator):
        for data in data_generator:
            x, y = data
            new_data = dateutil.parser.parse(x), y
            self.update_line(new_data)
        self.redraw_figure()

    def graph_max(self, data_generator):
        for data in data_generator:
            x, y = data
            new_data = dateutil.parser.parse(x), y
            self.update_max(new_data)
        self.redraw_figure()

    def graph_min(self, data_generator):
        for data in data_generator:
            x, y = data
            new_data = dateutil.parser.parse(x), y
            self.update_min(new_data)
        self.redraw_figure()

    def redraw_figure(self):
        # resizing figure
        self.ax1.relim()
        self.ax1.autoscale_view()

        try:
            self.fig1.canvas.draw()  # drawing figure
            self.fig1.show()         # display figure
        except ValueError as err:
            pass

    @staticmethod
    def display_graph(pause):
        plt.pause(pause)
