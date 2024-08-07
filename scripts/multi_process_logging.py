import logging
import logging.handlers
from multiprocessing import Pool, Queue, Process
import time
import traceback
import sys


def configure_listener():
    """ Configure the listener process to log to a file. """

    # Get the root logger
    root = logging.getLogger()

    # Add a file handler to the root logger
    file_handler = logging.FileHandler(filename='pool_logging.log', mode='w')

    # Define the message format
    formatter = logging.Formatter(
        '%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')

    # Apply the message format to the handler
    file_handler.setFormatter(formatter)

    # Add the file handler to the root logger
    root.addHandler(file_handler)


def listener_process(queue):
    """ Process that listens for log messages on the queue. """

    # Configure the listener process to log to a file
    configure_listener()

    # Process messages from the queue
    while True:

        try:

            # Get the next log record from the queue
            record = queue.get()

            # Sentinel to tell the listener to quit
            if record is None:
                break

            # Get the logger for the record
            logger = logging.getLogger(record.name)

            # Handle the log record using the registered log handlers
            logger.handle(record)

        # Handle exceptions gracefully
        except Exception as e:
            print(f'Whoops! Problem: {e}')
            traceback.print_exc(file=sys.stderr)


def configure_worker(queue):
    """ Configure the worker process to log to the queue. """

    # Create a QueueHandler to send log messages to a queue
    handler = logging.handlers.QueueHandler(queue)

    # Get the root logger
    root = logging.getLogger()

    # Add the QueueHandler to the root logger
    root.addHandler(handler)

    # Set the log level for the root logger
    root.setLevel(logging.DEBUG)


def worker_function(num):
    """ Function that will be executed by the worker processes. """

    # Each worker process needs to configure its logging
    queue = worker_function.queue
    configure_worker(queue)
    logger = logging.getLogger(__name__)

    # Worker process
    logger.debug(f'Worker processing number: {num}')
    time.sleep(1)
    logger.info(f'Worker finished processing number: {num}')
    return num * num


def init_worker(queue):
    """ Initialize the worker process with the queue.

    This is a workaround when working with the Pool class as it uses pickle to
    serialize objects that will be passed to the worker processes including
    shard objects like Queues.
    """
    worker_function.queue = queue


if __name__ == '__main__':

    # Create a Queue to pass log messages from worker processes to the listener
    log_queue = Queue()

    # Start the listener process
    listener = Process(target=listener_process, args=(log_queue,))
    listener.start()

    # Use a Pool to execute worker functions
    with Pool(5, initializer=init_worker, initargs=(log_queue,)) as pool:
        numbers = [1, 2, 3, 4, 5]
        results = pool.map(worker_function, numbers)

    # Stop the listener using the sentinel (None)
    log_queue.put(None)
    listener.join()

    # Print the results
    print('Results:', results)
