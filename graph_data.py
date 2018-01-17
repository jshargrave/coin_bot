import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import dateutil.parser


class GraphData:
    def __init__(self):
        self.fig1, (self.ax1) = plt.subplots(1)

        # Returns a tuple of line objects, thus the comma
        self.line1, self.max_line, self.min_line = self.ax1.plot([], [], 'r-', [], [], 'b.', [], [], 'y.')

        self.fig1.autofmt_xdate()
        self.xfmt = mdates.DateFormatter("%Y-%m-%d")
        self.ax1.xaxis.set_major_formatter(self.xfmt)

    def update_line(self, new_data):
        # appending new data to x and y lists
        self.line1.set_xdata(np.append(self.line1.get_xdata(), new_data[0]))
        self.line1.set_ydata(np.append(self.line1.get_ydata(), new_data[1]))

    def update_max(self, new_data):
        # appending new data to x and y lists
        self.max_line.set_xdata(np.append(self.max_line.get_xdata(), new_data[0]))
        self.max_line.set_ydata(np.append(self.max_line.get_ydata(), new_data[1]))

    def update_min(self, new_data):
        # appending new data to x and y lists
        self.min_line.set_xdata(np.append(self.min_line.get_xdata(), new_data[0]))
        self.min_line.set_ydata(np.append(self.min_line.get_ydata(), new_data[1]))

    def graph_data(self, data_generator):
        for i in data_generator:
            self.update_line((dateutil.parser.parse(i[1]), i[2]))
        self.redraw_figure()

    def graph_max(self, data_generator):
        for i in data_generator:
            self.update_max((dateutil.parser.parse(i[1]), i[2]))
        self.redraw_figure()

    def graph_min(self, data_generator):
        for i in data_generator:
            self.update_min((dateutil.parser.parse(i[1]), i[2]))
        self.redraw_figure()

    def redraw_figure(self):
        # resizing figure
        self.ax1.relim()
        self.ax1.autoscale_view()

        self.fig1.canvas.draw()  # drawing figure
        self.fig1.show()         # display figure
