## Solution Journal

### 1. Development Environment

| Category             | Details                   |
|----------------------|---------------------------|
| Programming Language | Python 3.12+              |
| Python IDE           | PyCharm Community Edition |
| Code style           | PEP-8, Google Doc Strings |
| Linting              | PyCharm built-in linter   |
| Testing              | Unittest                  |
| Version Control      | Git                       |
| Git Hosting          | GitHub                    |
| CI/CD                | GitHub Actions            |
| Documentation        | GitHub Pages, MkDocs      |


### 2. Multi-Processing

The task definition doesn't mention any performance requirements. We will 
concentrate on the implementation of the solution based on the task definition.
We will use the `multiprocessing` module to simulate multiple construction crews
working on the wall.

Processes are usesful for CPU-bound tasks, while threads are useful for 
I/O-bound tasks. CPU-bound tasks are tasks that require a lot of computations,
while I/O-bound tasks are tasks that require a lot of waiting for input/output
operations (from the network, disk, database, etc.).

The multiprocessing module allows us to create multiple processes that run
in parallel. Each process will simulate a construction crew working on a
section of the wall. We will use the `Pool` class to create a pool of worker
processes that will work on the wall sections.

The `Pool` class takes the number of worker processes as an argument. The most
common way to create a pool of worker processes is to use the `map` method. The
`map` method takes a function and an iterable as arguments. The function is
applied to each element of the iterable using the worker processes in the pool.

```python
from multiprocessing import Pool
import time
import os


def process_section(section):
    print(f"Processing section {section} in process {os.getpid()}")
    time.sleep(1)


def main():
    wall_profiles = [
        [10, 20],
        [10, 5],
        [20, 25]
    ]

    num_processes = 2

    # Get the sections
    sections = []
    for profile in wall_profiles:
        sections.extend(profile)

    # Do the work in parallel on the sections
    with Pool(num_processes) as pool:
        pool.map(process_section, sections)


if __name__ == "__main__":
    main()
```

Another possibility is to use the `starmap` method. The `starmap` method is
similar to the `map` method, but it takes an iterable of iterables as an
argument. Each inner iterable is unpacked and passed as arguments to the
function.

```python
from multiprocessing import Pool
import time
import os


def process_section(section, day):
    print(f"Processing section {section} on day {day} in process {os.getpid()}")
    time.sleep(1)
    

def main():
    
    wall_profiles = [
        [10, 20],
        [10, 5],
        [20, 25]
    ]

    num_processes = 2

    # Get the sections
    sections = []
    for profile in wall_profiles:
        sections.extend(profile)

    # Parallel execution of the sections with arguments
    with Pool(num_processes) as pool:
        pool.starmap(process_section, [(section, 1) for section in sections])

if __name__ == "__main__":
    main()
```

See also:

- https://pymotw.com/3/multiprocessing/index.html
- https://docs.python.org/3/library/multiprocessing.html

### 3. Multi-Process Logging

A challenge in the implementation is to log the progress of the construction
crews in a file that is shared between the processes.

> https://docs.python.org/3/howto/logging-cookbook.html
>
> Although logging is thread-safe, and logging to a single file from 
> multiple threads in a single process is supported, logging to a single 
> file from multiple processes is not supported, because there is no 
> standard way to serialize access to a single file across multiple 
> processes in Python. 

#### Proposal A : Listener Process, QueueHandler and shared Queue

```python
# https://docs.python.org/3/howto/logging-cookbook.html
# Section `Logging to a single file from multiple processes`

import logging
import logging.handlers
from multiprocessing import Pool, Queue, Process
from threading import Thread
import time


class LogListener(Thread):

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
```

#### Proposal B: Log everything in a managing process 

```python
```

See also:

- https://stackoverflow.com/questions/13522177/python-multiprocessing-logging-why-multiprocessing-get-logger
- https://pymotw.com/3/multiprocessing/basics.html#logging
- https://docs.python.org/3/library/logging.handlers.html#queuehandler
- https://github.com/getsentry/sentry-python

### 4. Proof of concept

In this step, we will create a prototype of the solution to check our 
understanding of the problem. The prototype will be just a simple Python 
script that takes the configuration as a python list and prints the daily
status of the wall.


### Introduction to Django and Django REST framework

### . Brainstorm the system design

- Microservice architecture
- REST API Design
- CI/CD pipeline
- Diagrams

### . Implement the REST API with Django

### . Implement unit tests for the backend

### . Feedback from a beta tester

### . Docstrings

### . Containerize the solution

### . Code review

### . Documentation

We will use MkDocs to build the documentation. The documentation will be
deployed to GitHub Pages. The documentation will contain at least the following
sections:

1. Problem
2. Solution
3. Installation
4. Rest API
5. CONTRIBUTING.md
6. README.md

### . Create the CI/CD pipeline

We will create a GitHub Actions workflow to run the tests on every push to the
main branch. We will also create a GitHub Actions workflow to build and push the
Docker image to Docker Hub on every release.

What we want:

1. Run the tests on every push to the main branch.
3. Build and push the Docker image to Docker Hub on each push.
4. Build the documentation and deploy it to GitHub Pages on every release.

### .First official release

Till now, we were in the pre-development phase. After the tag, changes will be
tracked using concrete issues in the commit messages.