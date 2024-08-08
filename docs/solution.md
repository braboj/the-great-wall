## Solution Journal

### Table of Contents

1. [Development Environment](#1-development-environment)
2. [Multi-Processing](#2-multi-processing)
3. [Multi-Process Logging](#3-multi-process-logging)
4. [Proof of Concept](#4-proof-of-concept)
5. [Introduction to Django](#5-introduction-to-django)

### 1. Development Environment

_Time spent: 1 hours_

#### Objectives
* Define the programming environment
* Define standards for further contributions
* Define the technology stack

#### 
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
| Containerization     | Docker                    |
| Web Framework        | Django                    |

### 2. Multi-Processing

_Time spent: 6 hours for research, prototyping and implementation_

Processes are usesful for CPU-bound tasks, while threads are useful for 
I/O-bound tasks. CPU-bound tasks are tasks that require a lot of computations,
while I/O-bound tasks are tasks that require a lot of waiting for input/output
operations (from the network, disk, database, etc.).

We will concentrate on the implementation of the solution based on the task 
definition. We will use the `multiprocessing` module to simulate multiple 
construction crews working on the wall.
 
The idea is to simulate a CPU bound task where each construction crew is working
to complete a task. In the end, we shall notice a performance improvement when
using multiple processes.

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

_Time spent: 4 hours for reading, prototyping and implementation_

A challenge in the implementation is to log the progress of the construction
crews in a file that is shared between the processes.

> https://docs.python.org/3/howto/logging-cookbook.html
>
> Although logging is thread-safe, and logging to a single file from 
> multiple threads in a single process is supported, logging to a single 
> file from multiple processes is not supported, because there is no 
> standard way to serialize access to a single file across multiple 
> processes in Python.

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

```python
import logging
import logging.handlers
import time
from multiprocessing import Process, Pool, Queue, current_process

# Constants
VOLUME_ICE_PER_FOOT = 195  # Material consumption per foot
COST_PER_VOLUME = 1900  # Cost of material per volume
WALL_HEIGHT = 30  # Fixed height of the wall


class LogListener(Process):

    def __init__(self, queue):
        super().__init__()

        # Set the queue to receive log messages
        self.queue = queue

        # Get the root logger
        self.root = logging.getLogger()

    def configure(self):
        """ Configure the listener process to log to a file. """

        # Define the message format
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)-8s %(processName)-10s - %(message)s'
        )

        # Add a console handler to the root logger
        console_handler = logging.StreamHandler()

        # Add a file handler to the root logger
        file_handler = logging.FileHandler(filename='pool_logging.log',
                                           mode='w')

        # Apply the message format to the handler
        file_handler.setFormatter(formatter)

        # Apply the message format to the handler
        console_handler.setFormatter(formatter)

        # Add the handlers to the root logger
        self.root.addHandler(file_handler)
        self.root.addHandler(console_handler)

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


class WallSection(object):
    """Represents a section of a wall."""

    def __init__(self, start_height, key_id=''):
        self.key_id = key_id
        self.start_height = start_height
        self.current_height = start_height
        self.log = logging.getLogger(__name__)

        # Set the name of the current process
        self.name = f'[Worker-{current_process().pid}]'

    def __repr__(self):
        return (f'WallSection('
                f'start_height={self.start_height}, '
                f'current_height={self.current_height}, '
                f'ice={self.get_ice()}, '
                f'cost={self.get_cost()}, '
                f'ready={self.is_ready()}'
                f')'
                )

    @staticmethod
    def configure(queue):
        log = logging.getLogger()

        # Create a QueueHandler to send log messages to a queue
        handler = logging.handlers.QueueHandler(queue)

        # Add the QueueHandler to the root logger
        log.addHandler(handler)

        # Set the log level for the root logger
        log.setLevel(logging.DEBUG)

    def is_ready(self):
        """Returns True if the wall section is ready to be constructed."""
        return self.current_height >= WALL_HEIGHT

    def get_ice(self):
        delta = self.current_height - self.start_height
        return delta * VOLUME_ICE_PER_FOOT

    def get_cost(self):
        return self.get_ice() * COST_PER_VOLUME

    def build(self):
        """Build the section by one foot per day."""

        original_name = current_process().name
        current_process().name = f'Worker-{original_name.split("-")[-1]}'

        # current_process().name = self.name

        if self.current_height < WALL_HEIGHT:
            self.current_height += 1

        self.log.info(f'Added 1 foot to section {self.key_id} to reach'
                      f' {self.current_height} feet')

        time.sleep(0.05)

        return self


class WallProfile(object):
    """Represents a profile of a wall."""

    def __init__(self, sections, full_name=''):
        self.full_name = full_name
        self.sections = sections
        self.log = logging.getLogger(__name__)

    def __repr__(self):
        return (f"WallProfile(full_name={self.full_name}, "
                f"ice={self.get_ice()}, "
                f"cost={self.get_cost()}, "
                f"ready={self.is_ready()}"
                f")"
                )

    def is_ready(self):
        """Returns True if the wall profile is ready to be constructed."""
        return all(section.is_ready() for section in self.sections)

    def get_ice(self):
        """Returns the total ice consumed by the wall profile."""
        return sum(section.get_ice() for section in self.sections)

    def get_cost(self):
        """Returns the total cost of the wall profile."""
        return self.get_ice() * COST_PER_VOLUME

    def build(self):
        """Builds the wall profile section by section."""

        # Build each section
        for section in self.sections:
            if not section.is_ready():
                section.build()

        return self


class WallBuilder(object):
    """Manages the construction of a wall."""

    def __init__(self):
        self.config_list = []
        self.wall_profiles = []
        self.sections = []
        self.log = logging.getLogger()

    @staticmethod
    def configure(queue):

        # Set the name of the current process
        current_process().name = 'Wall Manager'

        log = logging.getLogger()

        # Create a QueueHandler to send log messages to a queue
        handler = logging.handlers.QueueHandler(queue)

        # Add the QueueHandler to the root logger
        log.addHandler(handler)

        # Set the log level for the root logger
        log.setLevel(logging.DEBUG)

    @staticmethod
    def create_profile(heights, profile_id):
        sections = [WallSection(start_height) for start_height in heights]
        return WallProfile(sections=sections, full_name=f"P{profile_id:02d}")

    def set_config(self, config_list):
        self.config_list = config_list

    def get_sections(self):

        sections = []
        index = 0

        for profile in self.wall_profiles:
            for section in profile.sections:
                section.name = index
                sections.append(section)
                index += 1

        return sections

    def get_ice(self):
        return sum(section.get_ice() for section in self.sections)

    def get_cost(self):
        return sum(section.get_cost() for section in self.sections)

    def build(self, max_teams=None, days=None):

        #
        log_queue = Queue()

        self.configure(log_queue)

        # Start the listener process
        listener = LogListener(log_queue)
        listener.start()

        # Create the wall profiles
        self.wall_profiles = [
            self.create_profile(heights, index) for
            index, heights in enumerate(self.config_list)
        ]

        # Get the number of sections
        self.sections = self.get_sections()

        # Check if construction teams are specified
        if max_teams is None:
            max_teams = len(self.sections)

        # Check if construction days are specified
        if days is None:
            days = WALL_HEIGHT

        # Create a pool of workers
        pool = Pool(
            processes=max_teams,
            initializer=WallSection.configure,
            initargs=(log_queue,),
        )

        start_time = time.time()

        # Build the wall
        for day in range(days):

            # Check if all sections are ready
            if all(section.is_ready() for section in self.sections):
                break

            self.log.info(f"Day {day + 1}")

            # Map a section from a profile to a worker
            self.sections = pool.map(WallSection.build, self.sections)

        # Close the pool of workers
        pool.close()
        pool.join()

        end_time = time.time()

        # Log the results
        self.log.info('-' * 80)
        self.log.info(f'TOTAL ICE : {self.get_ice()}')
        self.log.info(f'TOTAL COST: {self.get_cost()}')
        self.log.info(f"Construction time: {end_time - start_time:.2f} seconds")

        # Stop the listener process using the sentinel
        log_queue.put(None)

        # Wait for the listener process to finish
        listener.join()

        return self


def main():
    # Define the wall configuration
    config_list = [
        [29, ] * 10,
        [29, ] * 10,
    ]

    # Create a wall builder
    builder = WallBuilder()
    builder.set_config(config_list)
    builder.build(max_teams=20, days=30)


if __name__ == "__main__":
    main()
```


### 5. Introduction to Django

Objectives:
* Project Setup
* Project Structure
* Django Views
* Routing of URLs
* Working app without database

```txt
# Create a django project:
django-admin startproject <replace_with_your_project_name>

# Start the Django project:
python manage.py runserver

# Create a new Django app
python manage.py startapp <replace_with_your_app_name>
```

| Category | Details                                                                                                                        |
|----------|--------------------------------------------------------------------------------------------------------------------------------|
| project  | A project is a collection of configurations and apps. One project can be composed of multiple apps, or a single app.           |
| app      | Web application that does something. An app usually is composed of a set of models (database tables), views, templates, tests. |
| model    | A model is a Python class represents a database table.                                                                         | 
| view     | A view is a Python function that takes a web request and returns a web response.                                               |
| template | A template is an HTML file that contains placeholders for dynamic content.                                                     |




See also:
- https://simpleisbetterthancomplex.com/series/beginners-guide/1.11/
- https://www.djangoproject.com/
- https://www.django-rest-framework.org/
- https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django


### . Brainstorm the system design

- Microservice architecture
- REST API Design
- CI/CD pipeline
- Class Diagrams

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