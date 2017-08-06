import config as cfg
import multiprocessing
import time


def main():
    pool = []

    #p = multiprocessing.Process(target=cfg.DB.retrieve_data, args=(1, ))
    #pool.append(p)
    p = multiprocessing.Process(target=cfg.graph_data())
    pool.append(p)

    for obj in pool:
        obj.start()

    print('here')
    time.sleep(10)


if __name__ == '__main__':
    main()

