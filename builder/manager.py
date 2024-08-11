# encoding: utf-8
from multiprocessing import Process, Pool, Queue, current_process
from abc import ABC, abstractmethod
from builder.errors import *
from builder.configurator import WallConfigurator

import logging.handlers
import logging
import time


class LogListener(Process):
    """Process that listens for log messages on a queue.

    Attributes:
        queue (Queue)   : A queue to receive log messages.
        logfile (str)   : The name of the log file.
        log (Logger)    : The root logger.
    """

    def __init__(self, queue, logfile='listener.log'):
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
        self.log = logging.getLogger()

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
        self.log.addHandler(file_handler)
        self.log.addHandler(console_handler)

    def stop(self):
        """Stop the log listener process."""

        # Flush the log handlers
        for handler in self.log.handlers:
            handler.flush()

        # Wait until the queue is empty
        while not self.queue.empty():
            time.sleep(0.1)

        # Stop the listener process using the sentinel message
        self.queue.put(None)

        # Wait for the listener process to finish
        self.join()

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
    def set_config(self, *args, **kwargs):
        """Sets an instance of the WallConfigurator class."""
        raise NotImplementedError

    @abstractmethod
    def is_ready(self, *args, **kwargs):
        """Check if the wall is ready to be constructed."""
        raise NotImplementedError

    @abstractmethod
    def get_ice(self, *args, **kwargs):
        """Get the total ice consumed by the wall."""
        raise NotImplementedError

    @abstractmethod
    def get_cost(self, *args, **kwargs):
        """Get the total cost of the wall."""
        raise NotImplementedError

    @abstractmethod
    def prepare(self, *args, **kwargs):
        """Prepare the wall builder for construction."""
        raise NotImplementedError

    @abstractmethod
    def build(self, *args, **kwargs):
        """Build something using the wall builder interface."""
        raise NotImplementedError

    @abstractmethod
    def validate(self):
        """Validate the attributes."""
        raise NotImplementedError


class SectionBuilder(WallBuilderAbc):
    """Represents a section of a wall.

    Attributes:
        section_id (int)    : The name of the wall section.
        profile_id (int)    : The profile ID of the wall section.
        start_height (int)  : The starting height of the wall section.
        current_height (int): The current height of the wall section.
        log (Logger)        : The logger for the wall section.
    """

    # All instances must share the same configuration
    config = WallConfigurator()

    def __init__(self, section_id=0, profile_id=None, start_height=0):
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
        self.day = 0

        # Set the logger for the wall builder
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.addHandler(logging.NullHandler())

    def __eq__(self, other):
        """Check if two wall sections are equal."""
        return all([
            self.section_id == other.section_id,
            self.profile_id == other.profile_id,
            self.start_height == other.start_height,
            self.current_height == other.current_height
        ])

    def __ne__(self, other):
        """Check if two wall sections are not equal."""
        return not self == other

    def __repr__(self):
        """Returns a string representation of the wall section."""

        return (f'WallSection(section_id={self.section_id}, '
                f'profile_id={self.profile_id}, '
                f'start_height={self.start_height}, '
                f'current_height={self.current_height}, '
                f'ready={self.is_ready()}'
                f')'
                )

    @classmethod
    def set_config(cls, config):
        cls.config = config
        return cls()

    def is_ready(self):
        """Returns True if the wall section is ready to be constructed."""
        return self.current_height >= self.config.target_height

    def get_ice(self):
        """Returns the ice consumed by the wall section."""
        delta = self.current_height - self.start_height
        return delta * self.config.volume_ice_per_foot

    def get_cost(self):
        """Returns the cost of the wall section."""
        return self.get_ice() * self.config.cost_per_volume

    def validate(self):
        """Validates the wall section configuration.

        This method validates the configuration of the wall section by checking
        the data types and values of the attributes. It raises exceptions if
        the attributes are not of the correct type or value.

        Raises:
            BuilderValidationError: If an attribute's type or value is invalid.

        Returns:
            SectionBuilder: The validated wall section instance.
        """

        # ----------------------------------------------------------------------
        # Validate current_height

        # Check the type of the start height
        if not isinstance(self.start_height, int):
            raise BuilderValidationError(
                info='The start height must be an integer'
            )

        # Check that the start height is between 0 and the target height
        if not 0 <= self.start_height <= self.config.target_height:
            raise BuilderValidationError(
                info='The start height must be between 0 and 30'
            )

        # ----------------------------------------------------------------------
        # Validate section_id

        # Check the type of section_id
        if not isinstance(self.section_id, int):
            raise BuilderValidationError(
                info='The section_id must be an integer'
            )

        # Check that the section_id is positive
        if self.section_id < 0:
            raise BuilderValidationError(
                info='The section_id must be a positive integer'
            )

        # ----------------------------------------------------------------------
        # Validate profile_id

        # Check the type of profile_id
        if not isinstance(self.profile_id, (int, type(None))):
            raise BuilderValidationError(
                info='The profile_id must be an integer'
            )

        # Check that the profile_id is positive
        if self.profile_id is not None and self.profile_id < 0:
            raise BuilderValidationError(
                info='The profile_id must be a positive integer'
            )

    @staticmethod
    def prepare(queue):
        """Configures the wall section to log to a queue.

        This method configures the wall section to log messages to a queue
        instead of the console. It creates a QueueHandler using a shared
        queue and adds it to the root logger for this process.

        Args:
            queue (Queue): A queue to receive log messages
        """

        # Get the root logger
        log = logging.getLogger()

        # Create a QueueHandler to send log messages to a queue
        handler = logging.handlers.QueueHandler(queue)

        # Add the QueueHandler to the root logger
        log.addHandler(handler)

        # Set the log level for the root logger
        log.setLevel(logging.INFO)

    def build(self, days=1):
        """Increment the section height with the build rate (foot/day).

        This method is part of a simulation process where each call to `build`
        increases the current height of the wall section by a predefined build
        rate. The method also renames the current worker process for better
        identification and logs the progress of the construction. It simulates
        time taken for the building process using a sleep function.

        Returns:
            SectionBuilder: The updated wall section instance.
        """

        # Rename the worker process
        original_name = current_process().name
        current_process().name = f'Worker-{original_name.split("-")[-1]}'

        # Build the wall section
        for day in range(days):

            # Check if the section is ready
            if self.is_ready():
                break

            # Build the wall for the day
            if self.current_height < self.config.target_height:
                self.current_height += self.config.build_rate
                self.day += 1

                # Log the build progress
                self.log.info(f'Added 1 foot to section {self.section_id} to reach'
                              f' {self.current_height} feet on day {self.day}')

            # Simulate CPU work
            time.sleep(self.config.cpu_worktime)

        # Return the updated wall section
        return self


class ProfileBuilder(WallBuilderAbc):
    """Represents a profile of a wall.

    Attributes:
        profile_id (int): The profile ID of the wall profile.
        sections (list): A list of wall sections in the profile.
        log (Logger): The logger for the wall profile.
    """

    # All instances must share the same configuration
    config = WallConfigurator()

    def __init__(self, profile_id=0, sections=None):
        """Initializes the wall profile.

        Args:
            profile_id (int)    : The profile ID of the wall profile.
            sections (list)     : A list of wall sections in the profile.
        """

        # Set the instance attributes
        self.profile_id = profile_id
        self.sections = sections or []

        # Set the logger for the wall builder
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.addHandler(logging.NullHandler())

    def __eq__(self, other):
        """Check if two wall profiles are equal."""
        return all([
            self.profile_id == other.profile_id,
            self.sections == other.sections
        ])

    def __ne__(self, other):
        """Check if two wall profiles are not equal."""
        return not self == other

    def __repr__(self):
        """Returns a string representation of the wall profile."""

        return (f"WallProfile(profile_id={self.profile_id}, "
                f"ice={self.get_ice()}, "
                f"cost={self.get_cost()}, "
                f"ready={self.is_ready()}"
                f")"
                )

    @classmethod
    def set_config(cls, config):
        """Sets an instance of the WallConfigurator class.

        Args:
            config (WallConfigurator): A configuration object.

        Returns:
            ProfileBuilder: An instance of the WallProfile class.
        """
        cls.config = config
        return cls()

    def is_ready(self):
        """Returns True if the wall profile is ready to be constructed."""

        # Check if there are any sections
        if not self.sections:
            return False

        # Check if all sections are ready
        else:
            return all(section.is_ready() for section in self.sections)

    def get_ice(self):
        """Returns the total ice consumed by the wall profile."""
        return sum(section.get_ice() for section in self.sections)

    def get_cost(self):
        """Returns the total cost of the wall profile."""
        return self.get_ice() * self.config.cost_per_volume

    def validate(self):
        """Validates the wall profile configuration.

        This method validates the configuration of the wall profile by checking
        the data types and values of the attributes. It raises exceptions if
        the attributes are not of the correct type or value.

        Raises:
            BuilderValidationError: If an attribute's type or value is invalid.

        Returns:
            ProfileBuilder: The validated wall profile instance.
        """

        # ----------------------------------------------------------------------
        # Validate profile_id

        # Check the type of profile_id
        if not isinstance(self.profile_id, int):
            raise BuilderValidationError(
                info='The profile_id must be an integer'
            )

        # Check that the profile_id is positive
        if not self.profile_id >= 0:
            raise BuilderValidationError(
                info='The profile_id must be a positive integer'
            )

        # ----------------------------------------------------------------------
        # Validate sections

        # Check that sections is a list
        if not isinstance(self.sections, list):
            raise BuilderValidationError(
                info='The sections must be a list'
            )

        # Check that all section elements are WallSection objects
        if not all(isinstance(s, SectionBuilder) for s in self.sections):
            raise BuilderValidationError(
                info='All sections must be WallSection objects'
            )

        # Check that the section size is between 1 and 2000
        if not 1 <= len(self.sections) <= self.config.max_section_count:
            raise BuilderValidationError(
                info='The sections count must be between 1 and 2000'
            )

        return self

    @staticmethod
    def prepare(queue):
        """Configures the wall section to log to a queue.

        This method configures the wall profile to log messages to a queue
        instead of the console. It creates a QueueHandler using a shared queue
        and adds it to the root logger for this process.

        Args:
            queue (Queue): A queue to receive log messages.
        """

        # Get the root logger
        log = logging.getLogger()

        # Create a QueueHandler to send log messages to a queue
        handler = logging.handlers.QueueHandler(queue)

        # Add the QueueHandler to the root logger
        log.addHandler(handler)

        # Set the log level for the root logger
        log.setLevel(logging.INFO)

    def build(self, days=1):
        """Builds all sections in the wall profile by the build rate.

        This method builds each section in the wall profile by calling the
        `build` method of each section. The method logs the progress of the
        construction and returns the updated wall profile instance.

        Returns:
            ProfileBuilder: The updated wall profile instance.
        """

        # Build each section in the wall profile
        for day in range(days):

            # Check if all sections are ready
            if self.is_ready():
                break

            # Build each section in the wall profile
            for section in self.sections:
                if not section.is_ready():
                    section.build()

        # Return the updated wall profile
        return self


class WallManagerAbc(ABC):
    """Abstract base class for the wall manager."""

    @abstractmethod
    def set_config(self, *args, **kwargs):
        """Sets an instance of the WallConfigurator class."""
        raise NotImplementedError

    @abstractmethod
    def is_ready(self, *args, **kwargs):
        """Check if the wall is ready to be constructed."""
        raise NotImplementedError

    @abstractmethod
    def get_ice(self, *args, **kwargs):
        """Get the total ice consumed by the wall."""
        raise NotImplementedError

    @abstractmethod
    def get_cost(self, *args, **kwargs):
        """Get the total cost of the wall."""
        raise NotImplementedError

    @abstractmethod
    def prepare(self, *args, **kwargs):
        """Prepare the wall manager for construction."""
        raise NotImplementedError

    @abstractmethod
    def build(self, *args, **kwargs):
        """Build something using the wall manager interface."""
        raise NotImplementedError

    @abstractmethod
    def validate(self):
        """Validate the attributes."""
        raise NotImplementedError


class WallManager(WallManagerAbc):
    """Manages the construction of a wall.

    Attributes:
        profiles (list): A list of wall profiles.
        sections (list): A list of wall sections.
        log (Logger): The logger for the wall builder.
        log_queue (Queue): A queue to receive log messages.
    """

    # All instances must share the same configuration
    config = WallConfigurator()

    def __init__(self, log_filepath='wall.log'):
        """Initializes the wall builder."""

        # Set the instance attributes
        self.profiles = []
        self.sections = []

        # Set the logger for the wall builder
        self.log_filepath = log_filepath
        self.log = logging.getLogger()
        self.log.addHandler(logging.NullHandler())

        # Create the log queue to receive log messages
        self.log_queue = Queue()
        self.prepare(self.log_queue)

    def report(self, start_time, end_time):
        """Log the results of the wall construction."""
        self.log.info('-' * 80)
        self.log.info(f'TOTAL ICE : {self.get_ice()}')
        self.log.info(f'TOTAL COST: {self.get_cost()}')
        self.log.info('-' * 80)
        self.log.info(f"Calculation time: {end_time - start_time:.2f} seconds")
        self.log.info('-' * 80)

    def parse_profile_list(self):
        """Parse the configuration list to create wall sections.

        This method parses the configuration list to create wall sections. It
        creates a wall profile for each row in the configuration list and
        populates the sections with the start heights.

        Returns:
            WallManager: The updated wall manager instance
        """

        # Helper variable to track the section ID
        section_id = 0

        # Clear the profiles and sections
        self.profiles.clear()
        self.sections.clear()

        # Parse the sections and profiles from the configuration list
        for row in self.config.profiles:

            profile_id = self.config.profiles.index(row)
            profile = ProfileBuilder(profile_id=profile_id)

            # Extract the sections from the row
            for column in row:
                section = SectionBuilder(
                    section_id=section_id,
                    profile_id=profile_id,
                    start_height=column
                )
                profile.sections.append(section)
                section_id += 1

            # Create a wall profile from the sections
            self.profiles.append(profile)
            self.sections.extend(profile.sections)

        return self

    def set_profile_list(self, profiles_list):
        """Set the profiles' list.

        Args:
            profiles_list (list): A list of profiles.

        Returns:
            WallManager: The updated wall manager instance.
        """

        # Set the profiles and sections
        self.config.profiles = profiles_list

        return self

    def update_profiles(self):
        """Update the profiles after calculations.

        This method is used to update the profiles after the calculations are
        complete. It filters the sections based on the profile ID and assigns
        the filtered sections to the profile.

        Returns:
            WallManager: An instance of the WallManager class.
        """

        for profile in self.profiles:
            profile_sections = list(
                filter(lambda x: x.profile_id == profile.profile_id,
                       self.sections)
            )
            profile.sections = profile_sections

        return self

    def get_profile(self, profile_id):
        """Get a profile by its ID.

        Args:
            profile_id (int): The profile ID of the wall profile.

        Returns:
            ProfileBuilder: The wall profile with the specified ID.
        """

        try:
            return next(
                profile for profile in self.profiles
                if profile.profile_id == profile_id
            )

        except StopIteration:
            raise BuilderError(f"Profile with ID {profile_id} not found.")

    def get_section(self, section_id):
        """Get a section by its ID.

        Args:
            section_id (int): The section ID of the wall section.

        Returns:
            SectionBuilder: The wall section with the specified ID.
        """

        try:
            return next(
                section for section in self.sections
                if section.section_id == section_id
            )

        except StopIteration:
            raise BuilderError(f"Section with ID {section_id} not found.")

    @classmethod
    def set_config(cls, config):
        """Sets an instance of the WallConfigurator class.

        Args:
            config (WallConfigurator): A configuration object.

        Returns:
            WallManager: An instance of the WallManager class.
        """

        cls.config = config
        return cls()

    def get_logs(self):
        """Get the log messages from a file."""

        logs = []

        with open(self.log_filepath, 'r') as file:
            for line in file:
                logs.append(line)

        # Convert the logs to a dictionary
        logs = {
            'logs': logs
        }

        return logs

    def is_ready(self):
        """Check if all wall sections are ready."""

        # Check if there are any sections
        if not self.sections:
            return False

        # Check if all sections are ready
        else:
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

        Raises:
            BuilderValidationError: If an attribute's type or value is invalid.

        Returns:
            WallManager: The validated wall manager instance.
        """

        profiles_list = self.config.profiles

        # Check that config_list is a list
        if not isinstance(profiles_list, list):
            raise BuilderValidationError(
                info='The config_list must be a list'
            )

        # Check that all elements of config_list are lists
        if not all(isinstance(element, list) for element in profiles_list):
            raise BuilderValidationError(
                info='All elements of config_list must be lists'
            )

        # Check that all elements of config_list are integers
        for i, profiles in enumerate(profiles_list):
            for j, section_height in enumerate(profiles):
                if not isinstance(section_height, int):
                    raise BuilderValidationError(
                        info=f'Element at index [{i}][{j}] is not an integer.'
                    )

        return self

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

        # Get the root logger for the wall builder
        log = logging.getLogger()

        """
        The following code is commented out. It is working as expected, but
        when the unit tests are started, something stays in the background
        and doesn't allow the tests to finish. The tests are hanging.
        
        Investigate the issue and fix it. It is a nice problem to practice
        debugging techniques on multiprocessing and logging.
        """
        # ----------------------------------------------------------------------
        # Create a QueueHandler to send log messages to a queue
        # handler = logging.handlers.QueueHandler(queue)

        # Add the QueueHandler to the root logger
        # log.addHandler(handler)
        # ----------------------------------------------------------------------

        # Set the log level for the root logger
        log.setLevel(logging.INFO)

    def build(self, days=1, num_teams=1):
        """Build the wall using a pool of workers.

        This method builds the wall using a pool of workers. Each worker is
        mapped to build a wall section.

        Args:
            days (int)      : The number of days to build the wall.
            num_teams (int) : The number of construction teams.

        Returns:
            WallManager: The updated wall builder instance.
        """

        # Start the log listener process
        log_listener = LogListener(
            queue=self.log_queue,
            logfile=self.log_filepath
        )
        log_listener.start()

        try:

            # Parse the profile list
            self.parse_profile_list()

            # Create a pool of workers
            pool = Pool(
                processes=num_teams,
                initializer=SectionBuilder.prepare,
                initargs=(self.log_queue,),
            )

            # Save the start timestamp
            start_time = time.time()

            # Build the wall
            for day in range(days):

                # Check if all sections are ready
                if self.is_ready():
                    break

                # Map a section from a profile to a worker
                self.sections = pool.starmap(
                    func=SectionBuilder.build,
                    iterable=[(section, days) for section in self.sections]
                )

            # No more work to be done
            pool.close()
            pool.join()

            # Save the end timestamp
            end_time = time.time()

            # Log the results
            self.report(start_time=start_time, end_time=end_time)

            # Update the profiles
            self.update_profiles()

        except Exception as e:
            raise BuilderError(f"An error occurred: {e}")

        finally:
            log_listener.stop()

        # Return the updated wall builder
        return self


def main():
    """Main function for testing the wall classes."""

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

    config = WallConfigurator(
        profiles=config_list,
    )

    # Create a wall builder
    builder = WallManager.set_config(config)
    builder.build(num_teams=20, days=30)
    # builder.build(num_teams=20, days=30)
    # builder.build(num_teams=20, days=1)

    # Profile 1
    # profile = builder.profiles[0]
    # print(profile)


if __name__ == "__main__":
    main()
