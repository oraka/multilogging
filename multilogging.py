import logging
import logging.handlers
import multiprocessing as mp
import time


def logging_worker(q):
    logger = logging.getLogger()
    h = logging.handlers.TimedRotatingFileHandler("worker.log", when="midnight", backupCount=20)
    f = logging.Formatter("%(asctime)s %(processName)-10s %(name)-10s %(levelname)-8s %(message)s")
    h.setFormatter(f)
    logger.addHandler(h)
    while True:
        logger.handle(q.get())


def worker(process_id, log_queue):
    h = logging.handlers.QueueHandler(log_queue)
    logger = logging.getLogger()
    logger.addHandler(h)
    logger.setLevel(logging.DEBUG)
    for i in range(10):
        logger.info(f"worker: {process_id} message #{i}")
        time.sleep(1)


def main():
    l = logging.getLogger()
    h = logging.handlers.TimedRotatingFileHandler("main.log", when="midnight", backupCount=20)
    f = logging.Formatter("%(asctime)s %(processName)-10s %(name)-10s %(levelname)-8s %(message)s")
    h.setFormatter(f)
    l.addHandler(h)
    log_queue = mp.Queue()
    logging_process = mp.Process(target=logging_worker, daemon=True, args=(log_queue,))
    logging_process.start()
    process_list = [mp.Process(target=worker, daemon=True, args=(i, log_queue)) for i in range(10)]
    [p.start() for p in process_list]
    logger = logging.getLogger()
    for i in range(10000):
        logger.error(f"main process {i}")
        print(f"main process {i}")
        time.sleep(0.5)


if __name__ == "__main__":
    main()
