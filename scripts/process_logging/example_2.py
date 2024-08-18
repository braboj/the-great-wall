# SuperFastPython.com
# example of logging from multiple processes in a process-safe manner
from random import random
from time import sleep
from logging.handlers import QueueHandler
import logging
from multiprocessing import (
    current_process,
    Process,
    Queue
)


def logger_process(queue):

    # Create a logger
    logger = logging.getLogger('app')

    # Configure a stream handler
    logger.addHandler(logging.StreamHandler())

    # Log all messages, debug and up
    logger.setLevel(logging.DEBUG)

    # Run forever
    while True:

        # Consume a log message, block until one arrives
        message = queue.get()

        # Check for shutdown
        if message is None:
            break

        # Log the message
        logger.handle(message)


# task to be executed in child processes
def task(queue):

    # Create a logger
    logger = logging.getLogger('app')

    # Add a handler that uses the shared queue
    logger.addHandler(QueueHandler(queue))

    # Log all messages, debug and up
    logger.setLevel(logging.DEBUG)

    # Get the current process
    process = current_process()

    # Report initial message
    logger.info(f'Child {process.name} starting.')

    # Simulate doing work
    for i in range(5):

        # report a message
        logger.debug(f'Child {process.name} step {i}.')

        # block
        sleep(random())

    # Report final message
    logger.info(f'Child {process.name} done.')


def main():

    # Create the shared queue
    queue = Queue()

    # Create a logger
    logger = logging.getLogger('app')

    # Add a handler that uses the shared queue
    logger.addHandler(QueueHandler(queue))

    # Log all messages, debug and up
    logger.setLevel(logging.DEBUG)

    # Start the logger process
    logger_p = Process(target=logger_process, args=(queue,))
    logger_p.start()

    # Report initial message
    logger.info('Main process started.')

    # Configure child processes
    processes = [Process(target=task, args=(queue,)) for i in range(5)]

    # start child processes
    for process in processes:
        process.start()

    # Wait for child processes to finish
    for process in processes:
        process.join()

    # Report final message
    logger.info('Main process done.')

    # Shutdown the queue correctly
    queue.put(None)


# protect the entry point
if __name__ == '__main__':

    for _ in range(3):
        main()