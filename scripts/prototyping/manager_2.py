# encoding: utf-8
from multiprocessing import Pool, Manager, current_process
from abc import ABC, abstractmethod
from builder.errors import *
from builder.configurator import WallConfigurator
from builder.validator import ConfigValidator

import logging.handlers
import logging
import time


class WallBuilderAbc(ABC):
    """Abstract base class for the wall actors."""

    # All instances of the base class must share the same configuration
    config = WallConfigurator()

    @classmethod
    def set_config(cls, config):
        """Sets an instance of the WallConfigurator class.

        Args:
            config (WallConfigurator): A configuration object.

        Returns:
            WallManager: An instance of the WallManager class.
        """

        cls.config = config

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
    def build(self, *args, **kwargs):
        """Build something using the wall builder interface."""
        raise NotImplementedError

    @abstractmethod
    def validate(self):
        """Validate the attributes."""
        raise NotImplementedError


class WallSection(WallBuilderAbc):
    """Represents a section of a wall.

    Attributes:
        section_id (int)    : The name of the wall section.
        profile_id (int)    : The profile ID of the wall section.
        start_height (int)  : The starting height of the wall section.
        current_height (int): The current height of the wall section.
        log (Logger)        : The logger for the wall section.

    Example:

        from builder.manager import WallSection

        # Build a wall section
        section = (
            WallSection(section_id=0, profile_id=0, start_height=28)
            .build()
            .build()
            .build()
        )

        # Check if the section is ready
        print(section.is_ready())

        # Get the ice consumed by the section
        print(section.get_ice())

        # Get the cost of the section
        print(section.get_cost())
    """

    # All instances must share the same configuration
    config = WallConfigurator()

    def __init__(self,
                 section_id=0,
                 profile_id=None,
                 start_height=0,
                 validator=ConfigValidator()
                 ):
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

        # Set the validator
        self.validator = validator

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
        """Validates the wall section instance."""

        self.validator.check_height(self.start_height)
        self.validator.check_primary_key(self.section_id)
        self.validator.check_foreign_key(self.profile_id)

    def build(self, days=1, queue=None):
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
        worker_name = f'Worker-{original_name.split("-")[-1]}'
        current_process().name = worker_name

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
                if queue:
                    queue.put(f'{worker_name:12s} : Added 1 foot to section '
                              f'{self.section_id} to reach '
                              f'{self.current_height} feet on day {self.day}')

            # Simulate CPU work
            time.sleep(self.config.cpu_worktime)

        # Return the updated wall section
        return self


class WallProfile(WallBuilderAbc):
    """Represents a profile of a wall.

    Attributes:
        profile_id (int): The profile ID of the wall profile.
        sections (list): A list of wall sections in the profile.
        log (Logger): The logger for the wall profile.

    Example:

        from builder.manager import WallProfile

        # Add a wall section to the profile
        sections = [
            WallSection(section_id=1, profile_id=1, start_height=28),
            WallSection(section_id=2, profile_id=1, start_height=28),
            WallSection(section_id=3, profile_id=1, start_height=28),
        ]

        # Build the wall profile
        profile = (
            WallProfile(profile_id=1, sections=sections)
            .build()
            .build()
            .build()
        )

        # Check if the profile is ready
        print(profile.is_ready())

        # Get the ice consumed by the profile
        print(profile.get_ice())

        # Get the cost of the profile
        print(profile.get_cost())
    """

    # All instances must share the same configuration
    config = WallConfigurator()

    def __init__(self,
                 profile_id=0,
                 sections=None,
                 validator=ConfigValidator()
                 ):
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

        # Set the validator
        self.validator = validator

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
            WallProfile: The validated wall profile instance.
        """

        # Check the instance attributes
        self.validator.check_primary_key(self.profile_id)
        self.validator.check_iterable(self.sections)
        self.validator.check_wall_profiles(self.sections)

        # Check each section in the wall profile
        for section in self.sections:
            section.validate()

        return self

    def build(self, days=1):
        """Builds all sections in the wall profile by the build rate.

        This method builds each section in the wall profile by calling the
        `build` method of each section. The method logs the progress of the
        construction and returns the updated wall profile instance.

        Returns:
            WallProfile: The updated wall profile instance.
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


class WallManager(WallBuilderAbc):
    """Manages the construction of a wall.

    Attributes:
        profiles (list): A list of wall profiles.
        sections (list): A list of wall sections.
        log (Logger): The logger for the wall builder.

    Example:

        from builder.manager import WallManager

        # Define the wall configuration
        config_list = [
            [21, 25, 28],
            [17],
            [17, 22, 17, 19, 17, ]
        ]

        # Create a wall builder
        builder = WallManager()

        # Set the profiles' config list
        builder.set_config_list(config_list)

        # Build the wall
        builder.build(num_teams=20, days=30)

        # Get the ice consumed by the wall
        print(builder.get_ice())

        # Get the cost of the wall
        print(builder.get_cost())
    """

    def __init__(self,
                 log_filepath='wall.log',
                 validator=ConfigValidator()
                 ):
        """Initializes the wall builder."""

        # Set the instance attributes
        self.profiles = []
        self.sections = []

        # Set the logger for the wall builder
        self.log_filepath = log_filepath
        self.log = logging.getLogger()

        # Set the validator
        self.validator = validator

        # Prepare the manager for logging
        self.enable_logging()

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

        return self

    def set_config_list(self, profiles_list):
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
            WallProfile: The wall profile with the specified ID.
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
            WallSection: The wall section with the specified ID.
        """

        try:
            return next(
                section for section in self.sections
                if section.section_id == section_id
            )

        except StopIteration:
            raise BuilderError(f"Section with ID {section_id} not found.")

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

        # Check each profile in the wall manager
        self.validator.check_iterable(self.profiles)
        for profile in self.profiles:
            profile.validate()

        # Check each section in the wall manager
        self.validator.check_iterable(self.sections)
        for section in self.sections:
            section.validate()

        # Check the profiles list
        self.validator.check_config_list(self.config.profiles)

        return self

    def enable_logging(self):

        # Check if the file handler exists
        log = logging.getLogger()

        # Define the message format
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)-8s - %(message)s'
        )

        # Add a console handler to the root logger
        console_handler = logging.StreamHandler()

        # Add a file handler to the root logger
        file_handler = logging.FileHandler(
            filename=self.log_filepath,
            mode='w'
        )

        # Add the handlers to the root logger
        log.addHandler(file_handler)
        log.addHandler(console_handler)

        # Set the formatter for the handlers
        for handler in self.log.handlers:
            handler.setFormatter(formatter)

        # Set the log level for the handlers
        for handler in self.log.handlers:
            handler.setLevel(logging.INFO)

        # Set the log level for the root logger
        log.setLevel(logging.INFO)

        return log

    def store_logs(self, queue):
        """Store the logs in the log file.

        This method stores the logs in the log file. It reads the logs from the
        queue and writes them to the log file.

        Args:
            queue (Queue): The queue containing the log messages.
        """

        # Open the log file in append mode
        with open(self.log_filepath, 'a') as file:

            # Read the logs from the queue
            while not queue.empty():
                log_message = queue.get()
                file.write(f'{log_message}\n')

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

        # Set the name of the current process
        current_process().name = 'Manager'

        # Parse the profile list
        self.parse_profile_list()

        self.log = self.enable_logging()

        # Create a manager to share the log queue (proxy)
        with Manager() as manager:

            # Create the proxy queue
            log_queue = manager.Queue()

            # Create a pool of workers
            with Pool(processes=num_teams) as pool:

                # Save the start timestamp
                # start_time = time.time()

                # Build the wall
                for day in range(days):

                    # Check if all sections are ready
                    if self.is_ready():
                        break

                    # Map a section from a profile to a worker
                    self.sections = pool.starmap(
                        func=WallSection.build,
                        iterable=[(section, days, log_queue) for section in self.sections]
                    )

                    # Save the end timestamp
                    # end_time = time.time()

            # After all processes have completed, process the results
            self.store_logs(log_queue)

            self.update_profiles()

        # Return the updated wall builder
        return self


def main():
    """Main function for testing the wall classes."""

    from rootdir import ROOT_DIR
    import os

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
    builder = WallManager(log_filepath=os.path.join(ROOT_DIR, 'data', 'wall.log'))
    builder.set_config(config)
    builder.build(num_teams=20, days=30)

    return builder.get_ice(), builder.get_cost()


if __name__ == "__main__":
    result = main()
    # print(result)
