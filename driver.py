import graph_data as gd
import bot_strategy as bs
from multiprocessing import Process


def main():
    pool = []
    pool.append(Process(target=bs.BotStrategy().monitor_price))

    for p in pool:
        p.start()

    print("Reached end of main")

if __name__ == '__main__':
    main()

