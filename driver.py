import bot_strategy as bs
from multiprocessing import Process


def main():
    pool = list()
    pool.append(Process(target=bs.BotStrategy().monitor_price))

    for p in pool:
        p.start()

    print("Reached end of main")

if __name__ == '__main__':
    main()
