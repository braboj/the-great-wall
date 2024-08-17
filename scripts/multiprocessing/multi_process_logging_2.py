import logging
import logging.handlers
import multiprocessing
from random import choice, random
import time

LEVELS = [logging.DEBUG, logging.INFO, logging.WARNING,
          logging.ERROR, logging.CRITICAL]

LOGGERS = ['a.b.c', 'd.e.f']

MESSAGES = [
    'Random message #1',
    'Random message #2',
    'Random message #3',
]


class Listener(object):

    @staticmethod
    def configure():
        """Configure logging for the listener process."""
        root = logging.getLogger()
        h = logging.FileHandler('mptest.log', 'w')
        f = logging.Formatter(
            '%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')
        h.setFormatter(f)
        root.addHandler(h)

    @staticmethod
    def process(queue, configurer):
        """Listen for log records on the queue and handle them."""
        configurer()
        while True:
            try:
                record = queue.get()
                if record is None:  # Sentinel value to terminate
                    break
                logger = logging.getLogger(record.name)
                logger.handle(record)  # Handle log record
            except Exception:
                import sys, traceback
                print('Whoops! Problem:', file=sys.stderr)
                traceback.print_exc(file=sys.stderr)


class Worker(object):

    @staticmethod
    def configure(queue):
        """Configure logging for worker processes."""
        h = logging.handlers.QueueHandler(queue)
        root = logging.getLogger()
        root.addHandler(h)
        root.setLevel(logging.DEBUG)

    @staticmethod
    def process(number):
        """Function executed by each worker in the pool."""
        name = multiprocessing.current_process().name
        print(f'Worker started: {number}')

        # Simulate work
        time.sleep(0.1)

        # Log a message
        logger = logging.getLogger()
        logger.info(f'Worker {number} message')

        print(f'Worker finished: {name}')


class Manager(object):

    @staticmethod
    def configure(queue):
        """Configure logging for worker processes."""
        h = logging.handlers.QueueHandler(queue)
        root = logging.getLogger()
        root.addHandler(h)
        root.setLevel(logging.DEBUG)

    @staticmethod
    def process():

        queue = multiprocessing.Queue(-1)

        Manager.configure(queue)

        # Start listener
        listener = multiprocessing.Process(
            target=Listener.process,
            args=(queue, Listener.configure)
        )
        listener.start()

        # Use a pool of worker processes
        with multiprocessing.Pool(
                processes=5,
                initializer=Worker.configure,
                initargs=(queue,)
        ) as pool:
            pool.map(Worker.process, range(5))

        # Log messages from the main thread
        logger = logging.getLogger("main")
        logger.info('Main thread message')

        # Signal the listener to terminate
        queue.put_nowait(None)
        listener.join()


def main():

    manager = Manager()
    manager.process()



if __name__ == '__main__':
    for _ in range(2):
        main()
