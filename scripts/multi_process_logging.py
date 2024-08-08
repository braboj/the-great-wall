import logging
import logging.handlers
from multiprocessing import Pool, Queue, Process
from threading import Thread
import time


class LogListener(Process):

    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.root = logging.getLogger()

    def configure(self):
        """ Configure the listener process to log to a file. """

        # Add a file handler to the root logger
        file_handler = logging.FileHandler(filename='pool_logging.log',
                                           mode='w')

        # Define the message format
        formatter = logging.Formatter(
            '%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')

        # Apply the message format to the handler
        file_handler.setFormatter(formatter)

        # Add the file handler to the root logger
        self.root.addHandler(file_handler)

    def run(self):
        """ Process that listens for log messages on the queue. """

        # Configure the listener process to log to a file
        self.configure()

        # Process messages from the queue
        while True:

            try:

                # Get the next log record from the queue
                record = self.queue.get()

                # Sentinel to tell the listener to quit
                if record is None:
                    break

                # Get the logger for the record
                logger = logging.getLogger(record.name)

                # Handle the log record using the registered log handlers
                logger.handle(record)

            # Handle exceptions gracefully
            except Exception as e:
                print(f'Exception: {e}')


class Worker(Process):

    def __init__(self, queue, num):
        super().__init__()
        self.queue = queue
        self.num = num

    @staticmethod
    def configure(queue):
        """ Configure the worker process to log to the queue. """

        root = logging.getLogger()

        # Create a QueueHandler to send log messages to a queue
        handler = logging.handlers.QueueHandler(queue)

        # Add the QueueHandler to the root logger
        root.addHandler(handler)

        # Set the log level for the root logger
        root.setLevel(logging.DEBUG)

    @staticmethod
    def execute(num):
        """ Function that will be executed by the worker processes. """

        # Each worker process needs to configure its logging
        logger = logging.getLogger(__name__)

        # Worker process
        logger.debug(f'Worker processing number: {num}')
        time.sleep(1)
        logger.info(f'Worker finished processing number: {num}')
        return num * num


def main():

    # Create a Queue to pass log messages from worker processes to the listener
    log_queue = Queue()

    # Start the listener process
    listener = LogListener(log_queue)
    listener.start()

    pool = Pool(
        processes=5,
        initializer=Worker.configure,
        initargs=(log_queue,)
    )

    results = pool.map(Worker.execute, [1, 2, 3, 4, 5])

    pool.close()
    pool.join()

    # Stop the listener using the sentinel (None)
    log_queue.put(None)
    listener.join()

    # Print the results
    print('Results:', results)


if __name__ == '__main__':
    main()