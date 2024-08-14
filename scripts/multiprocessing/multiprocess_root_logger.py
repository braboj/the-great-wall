import logging
import multiprocessing


def worker_process():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(processName)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    logger.info("This is a log message from the worker process.")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(processName)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()
    logger.info("This is a log message from the main process.")

    process = multiprocessing.Process(target=worker_process)
    process.start()
    process.join()
