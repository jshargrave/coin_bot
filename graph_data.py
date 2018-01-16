import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import dateutil.parser


class GraphData:
    def __init__(self):
        self.x = []
        self.y = []

        self.fig1, (self.ax1) = plt.subplots(1)
        self.fig1_num = self.fig1.number

        self.fig1.add_axes(self.ax1, label="ax1")
        self.line1, = self.ax1.plot(self.x, self.y, 'r-')  # Returns a tuple of line objects, thus the comma

        self.fig1.autofmt_xdate()
        self.xfmt = mdates.DateFormatter("%Y-%m-%d")
        self.ax1.xaxis.set_major_formatter(self.xfmt)

    def update_graph(self, new_data):
        # appending new data to x and y lists
        self.x.append(dateutil.parser.parse(new_data[0]))
        self.y.append(new_data[1])

        # setting new data
        self.line1.set_xdata(self.x)
        self.line1.set_ydata(self.y)

    def graph_data(self, data_generator):
        for i in data_generator:
            self.update_graph((i[1], i[2]))
        self.redraw_figure()

    def redraw_figure(self):
        # resizing figure
        self.ax1.relim()
        self.ax1.autoscale_view()

        self.fig1.canvas.draw()  # drawing figure
        self.fig1.show()         # display figure
