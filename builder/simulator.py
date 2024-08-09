from multiprocessing import Process, Pool, Queue, current_process
from abc import ABC, abstractmethod
from rootdir import ROOT_DIR

import logging
import logging.handlers
import time
import os
import math

# Constants
LOG_FILE = os.path.join(ROOT_DIR, 'data', 'wall_progress.log')
VOLUME_ICE_PER_FOOT = 195   # Material consumption per foot
COST_PER_VOLUME = 1900      # Cost of material per volume
TARGET_HEIGHT = 30          # Fixed height of the wall
SIMULATION_TIME = 0.01      # Simulated CPU work
MAX_SECTION_COUNT = 2000    # Maximum number of sections
MAX_WORKERS = 20            # Maximum number of workers
BUILD_RATE = 1              # Feet per day


class LogListener(Process):
    """Process that listens for log messages on a queue.

    Attributes:
        queue (Queue)       : A queue to receive log messages.
        logfile (str)       : The name of the log file.
        root_log (Logger)   : The root logger.
    """

    def __init__(self, queue, logfile=LOG_FILE):
        """Initializes the log listener process.

        Args:
            queue (Queue)   : A queue to receive log messages.
            logfile (str)   : The name of the log file.
        """

        # Initialize the parent class
        super().__init__()

        # Set the queue to receive log messages
        self.queue = queue

        # Set the log file name
        self.logfile = logfile

        # Get the root logger
        self.root_log = logging.getLogger()

    def configure(self):
        """Configure the listener process to log to a file."""

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

        # Apply the message format to the handler
        file_handler.setFormatter(formatter)

        # Apply the message format to the handler
        console_handler.setFormatter(formatter)

        # Add the handlers to the root logger
        self.root_log.addHandler(file_handler)
        self.root_log.addHandler(console_handler)

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
    """Abstract base class for the wall builder."""

    @abstractmethod
    def is_ready(self):
        """Check if the wall is ready to be constructed."""
        raise NotImplementedError

    @abstractmethod
    def get_ice(self):
        """Get the total ice consumed by the wall."""
        raise NotImplementedError

    @abstractmethod
    def get_cost(self):
        """Get the total cost of the wall."""
        raise NotImplementedError

    @abstractmethod
    def prepare(self, *args, **kwargs):
        """Prepare the wall builder for construction."""
        raise NotImplementedError

    @abstractmethod
    def build(self, *args, **kwargs):
        """Build the wall."""
        raise NotImplementedError

    @abstractmethod
    def validate(self):
        """Validate the wall builder configuration."""
        raise NotImplementedError


class WallSection(WallBuilderAbc):
    """Represents a section of a wall.

    Attributes:
        section_id (int): The name of the wall section.
        profile_id (int): The profile ID of the wall section.
        start_height (int): The starting height of the wall section.
        current_height (int): The current height of the wall section.
        log (Logger): The logger for the wall section.
    """

    def __init__(self, section_id, profile_id=None, start_height=0):
        """Initializes the wall section.

        Args:
            section_id (int): The section identifier
            profile_id (int): The profile ID of the wall section.
            start_height (int): The starting height of the wall section.
        """

        # Set the instance attributes
        self.section_id = section_id
        self.profile_id = profile_id
        self.start_height = start_height
        self.current_height = start_height
        self.log = logging.getLogger(__name__)

    def __repr__(self):
        """Returns a string representation of the wall section."""

        return (f'WallSection(section_id={self.section_id}, '
                f'profile_id={self.profile_id}, '
                f'start_height={self.start_height}, '
                f'current_height={self.current_height}, '
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
        """Validates the wall section configuration.

        This method validates the configuration of the wall section by checking
        the data types and values of the attributes. It raises exceptions if
        the attributes are not of the correct type or value.

        Raises:
            TypeError: If the data types of the attributes are incorrect.
            ValueError: If the values of the attributes are incorrect.
        """

        # ----------------------------------------------------------------------
        # Validate current_height

        # Check the type of the start height
        if not isinstance(self.start_height, int):
            raise TypeError('The start height must be an integer')

        # Check that the start height is between 0 and the target height
        if not 0 <= self.start_height <= TARGET_HEIGHT:
            raise ValueError('The start height must be between 0 and 30')

        # ----------------------------------------------------------------------
        # Validate section_id

        # Check the type of section_id
        if not isinstance(self.section_id, int):
            raise TypeError('The section_id must be an integer')

        # Check that the section_id is positive
        if not self.section_id >= 0:
            raise ValueError('The section_id must be a positive integer')

        # ----------------------------------------------------------------------
        # Validate profile_id

        # Check the type of profile_id
        if not isinstance(self.profile_id, (int, type(None))):
            raise TypeError('The profile_id must be an integer')

        # Check that the profile_id is positive
        if not self.profile_id >= 0:
            raise ValueError('The profile_id must be a positive integer')

    @staticmethod
    def prepare(queue):
        """Configures the wall section to log to a queue.

        This method configures the wall section to log messages to a queue
        instead of the console. It creates a QueueHandler and adds it to the
        root logger.

        Args:
            queue (Queue): A queue to receive log messages
        """

        # Get the root logger
        root_log = logging.getLogger()

        # Create a QueueHandler to send log messages to a queue
        handler = logging.handlers.QueueHandler(queue)

        # Add the QueueHandler to the root logger
        root_log.addHandler(handler)

        # Set the log level for the root logger
        root_log.setLevel(logging.INFO)

    def build(self):
        """Increment the section height with the build rate (foot/day).

        This method is part of a simulation process where each call to `build`
        increases the current height of the wall section by a predefined build
        rate. The method also renames the current worker process for better
        identification and logs the progress of the construction. It simulates
        time taken for the building process using a sleep function.

        Returns:
            WallSection: The updated wall section instance.
        """

        # Rename the worker process
        original_name = current_process().name
        current_process().name = f'Worker-{original_name.split("-")[-1]}'

        # Build the wall until the desired height is reached
        if self.current_height < TARGET_HEIGHT:
            self.current_height += BUILD_RATE

        # Log the build progress
        self.log.info(f'Added 1 foot to section {self.section_id} to reach'
                      f' {self.current_height} feet')

        # Simulate CPU work
        time.sleep(SIMULATION_TIME)

        # Return the updated wall section
        return self


class WallProfile(WallBuilderAbc):
    """Represents a profile of a wall.

    Attributes:
        profile_id (int): The profile ID of the wall profile.
        sections (list): A list of wall sections in the profile.
        log (Logger): The logger for the wall profile.
    """

    def __init__(self, profile_id, sections=None):
        """Initializes the wall profile.

        Args:
            profile_id (int): The profile ID of the wall profile.
            sections (list): A list of wall sections in the profile.
        """

        # Set the instance attributes
        self.profile_id = profile_id
        self.sections = sections or []
        self.log = logging.getLogger(__name__)

    def __repr__(self):
        """Returns a string representation of the wall profile."""

        return (f"WallProfile(profile_id={self.profile_id}, "
                f"ice={self.get_ice()}, "
                f"cost={self.get_cost()}, "
                f"ready={self.is_ready()}, "
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
        """Validates the wall profile configuration.

        This method validates the configuration of the wall profile by checking
        the data types and values of the attributes. It raises exceptions if
        the attributes are not of the correct type or value.
        """

        # ----------------------------------------------------------------------
        # Validate profile_id

        # Check the type of profile_id
        if not isinstance(self.profile_id, int):
            raise TypeError('The profile_id must be an integer')

        # Check that the profile_id is positive
        if not self.profile_id >= 0:
            raise ValueError('The profile_id must be a positive integer')

        # ----------------------------------------------------------------------
        # Validate sections

        # Check that sections is a list
        if not isinstance(self.sections, list):
            raise TypeError('The sections must be a list')

        # Check that all section elements are WallSection objects
        if not all(isinstance(section, WallSection) for section in self.sections):
            raise ValueError('All sections must be WallSection objects')

        # Check that the section size is between 1 and 2000
        if not 1 <= len(self.sections) <= MAX_SECTION_COUNT:
            raise MemoryError('The sections count must be between 1 and 2000')

    @staticmethod
    def prepare(queue):
        """Configures the wall section to log to a queue.

        This method configures the wall profile to log messages to a queue
        instead of the console. It creates a QueueHandler and adds it to the
        root logger.

        Args:
            queue (Queue): A queue to receive log messages.
        """

        # Get the root logger
        root_log = logging.getLogger()

        # Create a QueueHandler to send log messages to a queue
        handler = logging.handlers.QueueHandler(queue)

        # Add the QueueHandler to the root logger
        root_log.addHandler(handler)

        # Set the log level for the root logger
        root_log.setLevel(logging.INFO)

    def build(self):
        """Builds all sections in the wall profile by the build rate.

        This method builds each section in the wall profile by calling the
        `build` method of each section. The method logs the progress of the
        construction and returns the updated wall profile instance.

        Returns:
            WallProfile: The updated wall profile instance.
        """

        # Build each section
        for section in self.sections:
            if not section.is_ready():
                section.build()

        # Return the updated wall profile
        return self


class WallManager(WallBuilderAbc):
    """Manages the construction of a wall.

    Attributes:
        config_list (list): A list of wall section configurations.
        profiles (list): A list of wall profiles.
        sections (list): A list of wall sections.
        log (Logger): The logger for the wall builder.
        log_queue (Queue): A queue to receive log messages.
        log_listener (LogListener): A process to listen for log messages.
    """

    def __init__(self, config_list):
        """Initializes the wall builder.

        Args:
            config_list (list): A nested list of wall section configurations.
        """

        # Set the instance attributes
        self.config_list = config_list
        self.profiles = []
        self.sections = []

        # Set the logger for the wall builder
        self.log = logging.getLogger()
        self.log_queue = Queue()

        # Create and start the log listener process
        self.log_listener = LogListener(self.log_queue)
        self.log_listener.start()

    def report(self, start_time, end_time):
        self.log.info('-' * 80)
        self.log.info(f'TOTAL ICE : {self.get_ice()}')
        self.log.info(f'TOTAL COST: {self.get_cost()}')
        self.log.info('-' * 80)
        self.log.info(f"Calculation time: {end_time - start_time:.2f} seconds")
        self.log.info('-' * 80)

    def parse_config(self):
        """Parse the configuration list to create wall sections.

        This method parses the configuration list to create wall sections. It
        creates a wall profile for each row in the configuration list and
        populates the sections with the start heights.
        """

        # Helper variable to track the section ID
        section_id = 0

        # Parse the sections and profiles from the configuration list
        for row in self.config_list:

            profile_id = self.config_list.index(row)
            profile = WallProfile(profile_id=profile_id)

            # Extract the sections from the row
            for column in row:
                section = WallSection(
                    section_id=section_id,
                    profile_id=profile_id,
                    start_height=column
                )
                profile.sections.append(section)
                section_id += 1

            # Create a wall profile from the sections
            self.profiles.append(profile)
            self.sections.extend(profile.sections)

    def update_profiles(self):
        """Update the profiles after calculations.

        This method is used to update the profiles after the calculations are
        complete. It filters the sections based on the profile ID and assigns
        the filtered sections to the profile.
        """

        for profile in self.profiles:
            profile_sections = list(
                filter(lambda x: x.profile_id == profile.profile_id,
                       self.sections)
            )
            profile.sections = profile_sections

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
        """Validate the wall builder configuration.

        This method validates the configuration of the wall builder by checking
        the data types and values of the attributes. It raises exceptions if
        the attributes are not of the correct type or value.
        """

        # Check that config_list is a list
        if not isinstance(self.config_list, list):
            raise TypeError('The config_list must be a list')

        # Check that all elements of config_list are lists
        if not all(isinstance(heights, list) for heights in self.config_list):
            raise ValueError('All elements of config_list must be lists')

    @staticmethod
    def prepare(queue):
        """Configures the wall manager to log to a queue.

        This method configures the wall manager to log messages to a queue
        instead of the console. It creates a QueueHandler and adds it to the
        root logger.

        Args:
            queue (Queue): A queue to receive log messages.
        """

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

    def build(self, days=None, num_teams=None):
        """Build the wall using a pool of workers.

        This method builds the wall using a pool of workers. The workers are
        mapped to the build method of the wall sections. The method logs the
        progress of the construction and returns the updated wall builder
        instance.

        Args:
            days (int): The number of days to build the wall.
            num_teams (int): The number of construction teams.

        Returns:
            WallManager: The updated wall builder instance.
        """

        # Check if construction teams are specified
        if num_teams is None:
            num_teams = len(self.sections)

        # Calculate the days and roundup to the nearest integer
        if days is None:
            days = math.ceil(TARGET_HEIGHT / BUILD_RATE)

        # Configure the wall builder to log to the queue
        self.prepare(self.log_queue)

        # Parse the sections from the configuration list
        self.parse_config()

        # Create a pool of workers
        pool = Pool(
            processes=num_teams,
            initializer=WallSection.prepare,
            initargs=(self.log_queue,),
        )

        # Start the timer
        start_time = time.time()

        # Build the wall
        for day in range(days):

            # Check if all sections are ready
            if self.is_ready():
                break

            self.log.info(f"@ Calculation Distribution Day {day + 1}")

            # Map a section from a profile to a worker
            self.sections = pool.map(WallSection.build, self.sections)

        # End the timer
        end_time = time.time()

        # Close the pool of workers
        pool.close()
        pool.join()

        # Update the profiles
        self.update_profiles()

        # Log the results
        self.report(start_time=start_time, end_time=end_time)

        # Stop the listener process using the sentinel message
        self.log_queue.put(None)

        # Return the updated wall builder
        return self


def main():

    # Define the wall configuration
    # config_list = [
    #     [0, ] * 10,
    #     [0, ] * 10,
    # ]

    config_list = [
        [21, 25, 28],
        [17],
        [17, 22, 17, 19, 17, ]
    ]

    # Create a wall builder
    builder = WallManager(config_list)
    builder.build(num_teams=20, days=30)

    # Profile 1
    profile = builder.profiles[0]
    print(profile.get_ice())


if __name__ == "__main__":
    main()
