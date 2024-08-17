import logging
import logging.handlers
import multiprocessing
import time


class Listener(multiprocessing.Process):

    def __init__(self, queue, logfile='mptest.log'):
        super().__init__()
        self.queue = queue
        self.logfile = logfile
        self.log = logging.getLogger()

    def configure(self):
        """Configure logging for the listener process."""

        # Define the message format
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)-8s %(processName)-15s - %(message)s'
        )

        # Add a console handler to the root logger
        console_handler = logging.StreamHandler()

        # Add a file handler to the root logger
        file_handler = logging.FileHandler(
            filename=self.logfile,
            mode='w'
        )

        # Set the message format for the handlers
        for handler in [console_handler, file_handler]:
            handler.setFormatter(formatter)
            self.log.addHandler(handler)

    def run(self):
        """Listen for log records on the queue and handle them."""

        self.configure()

        while True:
            try:
                record = self.queue.get()
                if record is None:  # Sentinel value to terminate
                    break
                logger = logging.getLogger(record.name)
                logger.handle(record)  # Handle log record
            except Exception as e:
                import sys, traceback
                print('Whoops! Problem:', file=sys.stderr)
                traceback.print_exc(file=sys.stderr)


class Worker(object):

    def __init__(self):
        pass

    @staticmethod
    def prepare(queue):
        """Configure logging for worker processes."""
        h = logging.handlers.QueueHandler(queue)
        root = logging.getLogger()
        root.addHandler(h)
        root.setLevel(logging.DEBUG)

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
        h = logging.handlers.QueueHandler(queue)
        root = logging.getLogger()
        root.addHandler(h)
        root.setLevel(logging.DEBUG)

    def process(self):

        workers = [Worker() for _ in range(5)]

        self.prepare(self.queue)

        # Start listener
        listener = Listener(
            queue=self.queue
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
        self.queue.put_nowait(None)
        listener.join()


def main():
    manager = Manager()
    manager.process()


if __name__ == '__main__':
    for _ in range(5):
        main()
