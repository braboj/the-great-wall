# encoding: utf-8
from abc import ABC, abstractmethod
from builder.errors import BuilderConfigError
from pathlib import Path
from rootdir import ROOT_DIR
import configparser


class ConfiguratorAbc(ABC):
    """Abstract base class for configurators."""

    @abstractmethod
    def from_ini(self, file_path, *args, **kwargs):
        """Creates a configuration object from an INI file."""
        pass

    @abstractmethod
    def to_ini(self, file_path, *args, **kwargs):
        """Writes the configuration to an INI file."""
        pass


class WallConfigurator(object):
    """Configuration class for the wall builder.

    The benefits of using a configuration class are:

    1. It provides a single point of access to the configuration data.
    2. It allows for easy serialization and deserialization of the data.
    3. It protects the user's code from changes in the configuration data.

    Attributes:
        volume_ice_per_foot : The cubic feet of ice per foot height
        cost_per_volume     : The cost of ice per cubic foot
        target_height       : The target height of the wall (in feet)
        max_section_count   : The maximum number of sections
        build_rate          : The rate of building the wall (in feet per hour)
        num_workers         : The number of workers
        cpu_worktime        : The CPU work time (in seconds)
        profiles            : The list of profiles
        log_file            : The log file
        ini_file            : The INI file
    """

    LOG_FILE = ROOT_DIR + '/data/wall_progress.log'
    INI_FILE = ROOT_DIR + '/data/config.ini'

    def __init__(self,
                 volume_ice_per_foot=195,
                 cost_per_volume=1900,
                 target_height=30,
                 max_section_count=2000,
                 build_rate=1,
                 num_workers=20,
                 cpu_worktime=0.01,
                 profiles=None,
                 log_file=LOG_FILE,
                 ini_file=INI_FILE
                 ):
        """Initializes the configuration with default values.

        Args:
            volume_ice_per_foot : The cubic feet of ice per foot height
            cost_per_volume     : The cost of ice per cubic foot
            target_height       : The target height of the wall (in feet)
            max_section_count   : The maximum number of sections
            build_rate          : The rate of building the wall (feet per day)
            num_workers         : The number of workers
            cpu_worktime        : The CPU work time (in seconds)
            profiles            : The list of profiles
            log_file            : The log file
            ini_file            : The INI file
        """

        # Construction
        self.volume_ice_per_foot = volume_ice_per_foot
        self.cost_per_volume = cost_per_volume
        self.target_height = target_height
        self.max_section_count = max_section_count
        self.build_rate = build_rate

        # Task
        self.num_workers = num_workers
        self.cpu_worktime = cpu_worktime

        # Profiles
        self.profiles = profiles or []

        # Data storage
        self.log_file = log_file
        self.ini_file = ini_file

    def __repr__(self):
        """Returns a string representation of the configuration."""

        return (
            f"WallConfig(volume_ice_per_foot={self.volume_ice_per_foot}, "
            f"cost_per_volume={self.cost_per_volume}, "
            f"target_height={self.target_height}, "
            f"max_section_count={self.max_section_count}, "
            f"build_rate={self.build_rate}, "
            f"num_workers={self.num_workers}, "
            f"cpu_worktime={self.cpu_worktime}, "
            f"profiles={self.profiles}, "
            f"log_file={self.log_file}, "
            f"ini_file={self.ini_file})"
        )

    @classmethod
    def from_ini(cls, file_path=INI_FILE):
        """Creates a configuration object from an INI file.

        Args:
            file_path : The path to the INI file

        Returns:
            WallConfigurator : The configuration object
        """

        # Create the default configuration
        config = cls()

        # Check if the file exists
        path = Path(file_path)
        if not path.is_file():
            raise BuilderConfigError(
                info=f"Configuration file not found: {file_path}"
            )

        # Read the INI file
        parser = configparser.ConfigParser(allow_no_value=True)
        parser.read(file_path)

        # Get the construction section
        try:
            data = parser['Construction']
            config.volume_ice_per_foot = (data.getint('VOLUME_ICE_PER_FOOT'))
            config.cost_per_volume = data.getint('COST_PER_VOLUME')
            config.target_height = data.getint('TARGET_HEIGHT')
            config.max_section_count = data.getint('MAX_SECTION_COUNT')

        except Exception as e:
            raise BuilderConfigError(
                info=f"Error reading the construction section: {e}"
            )

        # Try to get the values from the section
        try:
            data = parser['Task']
            config.num_workers = data.getint('NUM_WORKERS')
            config.cpu_worktime = data.getfloat('CPU_WORKTIME')

        except ValueError as e:
            raise BuilderConfigError(
                info=f"Error reading the task section: {e}"
            )

        # Get the profiles section
        try:
            data = parser['Profiles']
            for key in data:
                # Convert the string to a list of integers
                config.profiles.append([int(x) for x in key.split()])

        except ValueError as e:
            raise BuilderConfigError(
                info=f"Error reading the profiles section: {e}"
            )

        # Return the configurator instance
        return config

    def to_ini(self, file_path=INI_FILE):
        """Writes the configuration to an INI file.

        Args:
            file_path : The path to the INI file

        Returns:
            None
        """

        # Create a ConfigParser object
        parser = configparser.ConfigParser(allow_no_value=True)

        try:
            parser.add_section('Construction')
            data = parser['Construction']
            data['VOLUME_ICE_PER_FOOT'] = str(self.volume_ice_per_foot)
            data['COST_PER_VOLUME'] = str(self.cost_per_volume)
            data['TARGET_HEIGHT'] = str(self.target_height)
            data['MAX_SECTION_COUNT'] = str(self.max_section_count)

        except Exception as e:
            raise BuilderConfigError(
                info=f"Error while setting the construction section: {e}"
            )

        # Add the task section
        try:
            parser.add_section('Task')
            task = parser['Task']
            task['NUM_WORKERS'] = str(self.num_workers)
            task['CPU_WORKTIME'] = str(self.cpu_worktime)

        except Exception as e:
            raise BuilderConfigError(
                info=f"Error while setting the task section: {e}"
            )

        # Write the configuration to a file
        with open(file_path, 'w') as file_path:

            # Write the configuration to the file
            parser.write(file_path)

            try:
                # Manually write the Profiles section
                file_path.write('[Profiles]\n')
                for profile in self.profiles:
                    file_path.write(f"{profile}\n")

            except Exception as e:
                raise BuilderConfigError(
                    info=f"Error writing the profiles section: {e}"
                )


def main():
    """Main function for testing the configurator."""

    # Read the configuration file
    config = WallConfigurator.from_ini()

    # Print the configuration
    print('Before:')
    print(config)

    # Change the configuration
    before = config.num_workers
    config.num_workers += 1

    # Write the configuration file
    config.to_ini()

    # Read the configuration file again
    config = WallConfigurator.from_ini()
    after = config.num_workers

    # Print the configuration
    print('After:')
    print(config)

    # Compare the new value
    assert (after - before) == 1


if __name__ == "__main__":
    main()
