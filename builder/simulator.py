import logging
import logging.handlers
import time
from multiprocessing import Process, Pool, Queue, current_process
from abc import ABC, abstractmethod

# Constants
VOLUME_ICE_PER_FOOT = 195   # Material consumption per foot
COST_PER_VOLUME = 1900      # Cost of material per volume
TARGET_HEIGHT = 30          # Fixed height of the wall
SIMULATION_TIME = 0.01      # Simulated CPU work
MAX_SECTION_COUNT = 2000    # Maximum number of sections


class LogListener(Process):
    """Process that listens for log messages on a queue.

    Attributes:
        queue (Queue): A queue to receive log messages.
        root (Logger): The root logger.
    """

    def __init__(self, queue):
        """Initializes the log listener process.

        Args:
            queue (Queue): A queue to receive log messages.
        """

        # Initialize the parent class
        super().__init__()

        # Set the queue to receive log messages
        self.queue = queue

        # Get the root logger
        self.root = logging.getLogger()

    def configure(self):
        """Configure the listener process to log to a file."""

        # Define the message format
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)-8s %(processName)-15s - %(message)s'
        )

        # Add a console handler to the root logger
        console_handler = logging.StreamHandler()

        # Add a file handler to the root logger
        file_handler = logging.FileHandler(filename='../tracker/pool_logging.log',
                                           mode='w')

        # Apply the message format to the handler
        file_handler.setFormatter(formatter)

        # Apply the message format to the handler
        console_handler.setFormatter(formatter)

        # Add the handlers to the root logger
        self.root.addHandler(file_handler)
        self.root.addHandler(console_handler)

    def run(self):
        """Process that listens for log messages on the queue."""

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


class WallBuilderAbc(ABC):

    @abstractmethod
    def is_ready(self):
        raise NotImplementedError

    @abstractmethod
    def get_ice(self):
        raise NotImplementedError

    @abstractmethod
    def get_cost(self):
        raise NotImplementedError

    @abstractmethod
    def configure(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def build(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def validate(self):
        raise NotImplementedError


class WallSection(WallBuilderAbc):
    """Represents a section of a wall.

    Attributes:
        start_height (int): The starting height of the wall section.
        current_height (int): The current height of the wall section.
        log (Logger): The logger for the wall section.
    """

    def __init__(self, start_height, name=''):
        """Initializes the wall section.

        Args:
            start_height (int): The starting height of the wall section.
            name (str): The name of the wall section.
        """

        # Set the instance attributes
        self.name = name
        self.start_height = start_height
        self.current_height = start_height
        self.log = logging.getLogger(__name__)

    def __repr__(self):
        """Returns a string representation of the wall section."""

        return (f'WallSection('
                f'start_height={self.start_height}, '
                f'current_height={self.current_height}, '
                f'ice={self.get_ice()}, '
                f'cost={self.get_cost()}, '
                f'ready={self.is_ready()}'
                f')'
                )

    def is_ready(self):
        """Returns True if the wall section is ready to be constructed."""
        return self.current_height >= TARGET_HEIGHT

    def get_ice(self):
        """Returns the ice consumed by the wall section."""
        delta = self.current_height - self.start_height
        return delta * VOLUME_ICE_PER_FOOT

    def get_cost(self):
        """Returns the cost of the wall section."""
        return self.get_ice() * COST_PER_VOLUME

    def validate(self):

        # Check the type of the start height
        if not isinstance(self.start_height, int):
            raise TypeError('The start height must be an integer')

        # Check that the start height is between 0 and the target height
        if not 0 <= self.start_height <= TARGET_HEIGHT:
            raise ValueError('The start height must be between 0 and 30')

        # Check that name is a string
        if not isinstance(self.name, str):
            raise TypeError('The name must be a string')

    @staticmethod
    def configure(queue):
        """Configures the wall section to log to a queue."""

        log = logging.getLogger()

        # Create a QueueHandler to send log messages to a queue
        handler = logging.handlers.QueueHandler(queue)

        # Add the QueueHandler to the root logger
        log.addHandler(handler)

        # Set the log level for the root logger
        log.setLevel(logging.DEBUG)

    def build(self):
        """Build the section by one foot per day."""

        # Rename the worker process
        original_name = current_process().name
        current_process().name = f'Worker-{original_name.split("-")[-1]}'

        # Build the wall until the desired height is reached
        if self.current_height < TARGET_HEIGHT:
            self.current_height += 1

        # Log the build progress
        self.log.info(f'Added 1 foot to section {self.name} to reach'
                      f' {self.current_height} feet')

        # Simulate CPU work
        time.sleep(SIMULATION_TIME)

        # Return the updated wall section
        return self


class WallProfile(WallBuilderAbc):
    """Represents a profile of a wall."""

    def __init__(self, sections, name=''):
        """Initializes the wall profile."""

        # Set the instance attributes
        self.name = name
        self.sections = sections
        self.log = logging.getLogger(__name__)

    def __repr__(self):
        """Returns a string representation of the wall profile."""

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

    def validate(self):

        # Check that sections is a list
        if not isinstance(self.sections, list):
            raise TypeError('The sections must be a list')

        # Check that all section elements are WallSection objects
        if not all(isinstance(section, WallSection) for section in self.sections):
            raise ValueError('All sections must be WallSection objects')

        # Check that the section size is between 1 and 2000
        if not 1 <= len(self.sections) <= MAX_SECTION_COUNT:
            raise MemoryError('The sections count must be between 1 and 2000')

        # Check that the name is a string
        if not isinstance(self.name, str):
            raise TypeError('The name must be a string')

    def configure(self, queue):
        """Configures the wall profile."""

        # Get the logger for the wall profile
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

        # Return the updated wall profile
        return self


class WallBuilderSimulator(WallBuilderAbc):
    """Manages the construction of a wall."""

    def __init__(self):
        """Initializes the wall builder."""

        # Set the instance attributes
        self.config_list = []
        self.wall_profiles = []
        self.sections = []
        self.log = logging.getLogger()

    def report(self, start_time, end_time):
        self.log.info('-' * 80)
        self.log.info(f'TOTAL ICE : {self.get_ice()}')
        self.log.info(f'TOTAL COST: {self.get_cost()}')
        self.log.info('-' * 80)
        self.log.info(f"Calculation time: {end_time - start_time:.2f} seconds")

    @staticmethod
    def create_profile(heights, profile_id):
        """Creates a wall profile with the specified heights."""

        # Create a wall profile with the specified heights
        sections = [WallSection(start_height) for start_height in heights]

        # Return the wall profile
        return WallProfile(sections=sections, name=f"P{profile_id:02d}")

    def set_config(self, config_list):
        """Sets the configuration for the wall builder."""

        # Set the configuration list
        self.config_list = config_list

    def get_sections(self):
        """Returns a list of wall sections from the wall profiles."""

        # Helper variables
        sections = []
        index = 0

        # Get the sections from the wall profiles
        for profile in self.wall_profiles:
            for section in profile.sections:
                section.name = index
                sections.append(section)
                index += 1

        # Return the list of wall sections
        return sections

    def is_ready(self):
        """Check if all wall sections are ready."""
        return all(section.is_ready() for section in self.sections)

    def get_ice(self):
        """Get the total ice consumed by the wall."""
        return sum(section.get_ice() for section in self.sections)

    def get_cost(self):
        """Get the total cost of the wall."""
        return sum(section.get_cost() for section in self.sections)

    def validate(self):

        # Check that config_list is a list
        if not isinstance(self.config_list, list):
            raise TypeError('The config_list must be a list')

        # Check that all elements of config_list are lists
        if not all(isinstance(heights, list) for heights in self.config_list):
            raise ValueError('All elements of config_list must be lists')

    @staticmethod
    def configure(queue):

        # Set the name of the current process
        current_process().name = 'Manager'

        # Get the logger for the wall builder
        log = logging.getLogger()

        # Create a QueueHandler to send log messages to a queue
        handler = logging.handlers.QueueHandler(queue)

        # Add the QueueHandler to the root logger
        log.addHandler(handler)

        # Set the log level for the root logger
        log.setLevel(logging.DEBUG)

    def build(self, max_teams=None, days=None):

        # Check if construction teams are specified
        if max_teams is None:
            max_teams = len(self.sections)

        # Check if the calculation days are specified
        if days is None:
            days = TARGET_HEIGHT

        # Create a queue for logging
        log_queue = Queue()

        # Configure the wall builder to log to the queue
        self.configure(log_queue)

        # Start the listener process
        listener = LogListener(log_queue)
        listener.start()

        # Create the wall profiles from the configuration list
        self.wall_profiles = [
            self.create_profile(heights, index) for
            index, heights in enumerate(self.config_list)
        ]

        # Get the number of sections
        self.sections = self.get_sections()

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

            self.log.info(f"@ Calculation Distribution Day {day + 1}")

            # Map a section from a profile to a worker
            self.sections = pool.map(WallSection.build, self.sections)

        # Close the pool of workers
        pool.close()
        pool.join()

        end_time = time.time()

        # Log the results
        self.report(start_time=start_time, end_time=end_time)

        # Stop the listener process using the sentinel
        log_queue.put(None)

        # Wait for the listener process to finish
        listener.join()

        # Return the updated wall builder
        return self


def main():
    # Define the wall configuration
    config_list = [
        [0, ] * 10,
        [0, ] * 10,
    ]

    # Create a wall builder
    builder = WallBuilderSimulator()
    builder.set_config(config_list)
    builder.build(max_teams=1, days=30)


if __name__ == "__main__":
    main()
