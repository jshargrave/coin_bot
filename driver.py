from data_processing import DataProcessing
import datetime


def main():
    DP = DataProcessing()

    # Historical
    line_generator = DP.bot_d.select_all("BitcoinHistorical")
    DP.graph_d_h.graph_data(line_generator)

    max_generator = DP.local_max_generator(DP.bot_d.select_all("BitcoinHistorical"))
    DP.graph_d_h.graph_max(max_generator)

    min_generator = DP.local_min_generator(DP.bot_d.select_all("BitcoinHistorical"))
    DP.graph_d_h.graph_min(min_generator)

    # RealTime
    line_generator = DP.bot_d.select_all("BitcoinRealTime")
    DP.graph_d_rt.graph_data(line_generator)

    max_generator = DP.local_max_generator(DP.bot_d.select_all("BitcoinRealTime"))
    DP.graph_d_rt.graph_max(max_generator)

    min_generator = DP.local_min_generator(DP.bot_d.select_all("BitcoinRealTime"))
    DP.graph_d_rt.graph_min(min_generator)

    while True:
        data = DP.cd_api.get_btc_price()
        DP.bot_d.insert("BitcoinRealTime", [data])
        DP.graph_d_rt.graph_data(DP.bot_d.select_new("BitcoinRealTime"))

        sleep_time = datetime.datetime.now() + datetime.timedelta(seconds=15)
        while sleep_time > datetime.datetime.now():
            DP.graph_d_rt.display_graph(0.0001)
            DP.graph_d_h.display_graph(0.0001)


if __name__ == '__main__':
    main()
