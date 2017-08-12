import bot_strategy as bs
from multiprocessing import Process
import bot_api as ba
import config as cfg

def main():
    pool = list()
    pool.append(Process(target=bs.BotStrategy().monitor_price))
    #pool.append(Process(target=bs.BotStrategy().monitor_price_simulator()))

    for p in pool:
        p.start()

    print("Reached end of main")

if __name__ == '__main__':
    main()
