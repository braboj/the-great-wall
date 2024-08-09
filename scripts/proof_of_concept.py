import logging
import logging.handlers
import time
from multiprocessing import Process, Pool, Queue, current_process
from abc import ABC, abstractmethod

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

    def __init__(self, start_height, name=''):
        self.name = name
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

        self.log.info(f'Added 1 foot to section {self.name} to reach'
                      f' {self.current_height} feet')

        time.sleep(0.05)

        return self


class WallProfile(object):
    """Represents a profile of a wall."""

    def __init__(self, sections, name=''):
        self.name = name
        self.sections = sections
        self.log = logging.getLogger(__name__)

    def __repr__(self):
        return (f"WallProfile(full_name={self.name}, "
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

    def configure(self, queue):
        """Configures the wall profile."""

        log = logging.getLogger()

        # Create a QueueHandler to send log messages to a queue
        handler = logging.handlers.QueueHandler(queue)

        # Add the QueueHandler to the root logger
        log.addHandler(handler)

        # Set the log level for the root logger
        log.setLevel(logging.DEBUG)

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

    def add_profile(self, profile):
        self.wall_profiles.append(profile)

    def remove_profile(self, profile):
        self.wall_profiles.remove(profile)

    @staticmethod
    def create_profile(heights, profile_id):
        sections = [WallSection(start_height) for start_height in heights]
        return WallProfile(sections=sections, name=f"P{profile_id:02d}")

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

    def is_ready(self):
        return all(section.is_ready() for section in self.sections)

    def get_ice(self):
        return sum(section.get_ice() for section in self.sections)

    def get_cost(self):
        return sum(section.get_cost() for section in self.sections)

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
            if self.is_ready():
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
