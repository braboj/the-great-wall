import logging
from logging.handlers import QueueListener, QueueHandler
import multiprocessing
import time


class Worker(object):

    @staticmethod
    def prepare(queue):
        """Configure logging for worker processes."""

        # Get the root logger
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)

        # Add a QueueHandler to the root logger
        handler = QueueHandler(queue)
        root.addHandler(handler)

    def build(self, number):
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

    def __init__(self):
        self.queue = multiprocessing.Queue(-1)
        self.log = logging.getLogger("main")

    @staticmethod
    def prepare(queue):
        """Configure logging for worker processes."""

        # Get the root logger
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)

        # Add a QueueHandler to the root logger
        handler = logging.handlers.QueueHandler(queue)
        root.addHandler(handler)

    def process(self):

        workers = [Worker() for _ in range(5)]

        self.prepare(self.queue)

        # Start listener
        listener = QueueListener(
            self.queue,
            *logging.getLogger().handlers
        )
        listener.start()

        # Use a pool of worker processes
        with multiprocessing.Pool(5, Worker.prepare, (self.queue,)) as pool:
            pool.starmap(
                Worker.build,
                [(worker, index) for index, worker in enumerate(workers)]
            )

        # Log messages from the main thread
        self.log.info('Main thread message')

        # Signal the listener to terminate
        listener.stop()


def main():
    manager = Manager()
    manager.process()


if __name__ == '__main__':

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()]
    )

    for _ in range(5):
        main()
