import config as cfg
import multiprocessing
import time
import graph_data as gd


def main():
    pool = []

    #p = multiprocessing.Process(target=cfg.DB.retrieve_data, args=(1, ))
    #pool.append(p)
    p = multiprocessing.Process(target=gd.GraphChart().real_time_graph(86400, 1, 0.2))
    pool.append(p)

    for obj in pool:
        obj.start()

    print('here')
    time.sleep(10)


if __name__ == '__main__':
    main()

