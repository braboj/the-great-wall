# encoding: utf-8
import json
from abc import ABC, abstractmethod
from builder.errors import BuilderConfigError
from pathlib import Path
import configparser

DEFAULT_LOG_FILE = 'wall_progress.log'
DEFAULT_INI_FILE = 'wall.ini'

# These constants are meant to be private and should not be used directly
# in the user's code. The WallConfigurator class provides a single point of
# access to the configuration data.

_VOLUME_ICE_PER_FOOT_ = 195  # Material consumption per foot
_COST_PER_VOLUME_ = 1900  # Cost of material per volume
_TARGET_HEIGHT_ = 30  # Fixed height of the wall
_SIMULATION_TIME_ = 0.01  # Simulated CPU work
_MAX_SECTION_COUNT_ = 2000  # Maximum number of sections
_MAX_WORKERS_ = 20  # Maximum number of workers
_BUILD_RATE_ = 1  # Feet per day
_PROFILES_ = [[21, 25, 28], [17], [17, 22, 17, 19, 17,]]


class ConfiguratorAbc(ABC):
    """Abstract base class for configurators."""

    @abstractmethod
    def get_params(self):
        """Returns the configuration parameters."""
        raise NotImplementedError

    @abstractmethod
    def set_params(self, params):
        """Sets the configuration parameters."""
        raise NotImplementedError

    @abstractmethod
    def from_ini(self, file_path, *args, **kwargs):
        """Creates a configuration object from an INI file."""
        raise NotImplementedError

    @abstractmethod
    def to_ini(self, file_path, *args, **kwargs):
        """Writes the configuration to an INI file."""
        raise NotImplementedError

    @abstractmethod
    def validate(self, *args, **kwargs):
        """Validates the configuration data."""
        raise NotImplementedError


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
        num_teams         : The number of workers
        cpu_worktime        : The CPU work time (in seconds)
        profiles        : The list of profiles
    """

    def __init__(self,
                 volume_ice_per_foot=195,
                 cost_per_volume=1900,
                 target_height=30,
                 max_section_count=2000,
                 build_rate=1,
                 num_teams=20,
                 cpu_worktime=0.01,
                 profiles=None,
                 ):
        """Initializes the configuration with default values.

        Args:
            volume_ice_per_foot : The cubic feet of ice per foot height
            cost_per_volume     : The cost of ice per cubic foot
            target_height       : The target height of the wall (in feet)
            max_section_count   : The maximum number of sections
            build_rate          : The rate of building the wall (feet per day)
            num_teams           : The number of workers
            cpu_worktime        : The CPU work time (in seconds)
            profiles            : The list of profiles
        """

        # Construction
        self.volume_ice_per_foot = volume_ice_per_foot
        self.cost_per_volume = cost_per_volume
        self.target_height = target_height
        self.max_section_count = max_section_count
        self.build_rate = build_rate

        # Task
        self.num_teams = num_teams
        self.cpu_worktime = cpu_worktime

        # Profiles
        self.profiles = profiles or []

    def __repr__(self):
        """Returns a string representation of the configuration."""

        return (
            f"WallConfig(volume_ice_per_foot={self.volume_ice_per_foot}, "
            f"cost_per_volume={self.cost_per_volume}, "
            f"target_height={self.target_height}, "
            f"max_section_count={self.max_section_count}, "
            f"build_rate={self.build_rate}, "
            f"num_workers={self.num_teams}, "
            f"cpu_worktime={self.cpu_worktime}, "
            f"profiles={self.profiles}, "
        )

    def get_params(self):

        return {
            'volume_ice_per_foot': self.volume_ice_per_foot,
            'cost_per_volume': self.cost_per_volume,
            'target_height': self.target_height,
            'max_section_count': self.max_section_count,
            'build_rate': self.build_rate,
            'num_teams': self.num_teams,
            'cpu_worktime': self.cpu_worktime,
            'profiles': self.profiles,
        }

    def set_params(self, params):

        # Set the configuration parameters
        self.volume_ice_per_foot = params.get('volume_ice_per_foot', _VOLUME_ICE_PER_FOOT_)
        self.cost_per_volume = params.get('cost_per_volume', _COST_PER_VOLUME_)
        self.target_height = params.get('target_height', _TARGET_HEIGHT_)
        self.max_section_count = params.get('max_section_count', _MAX_SECTION_COUNT_)
        self.build_rate = params.get('build_rate', _BUILD_RATE_)
        self.num_teams = params.get('num_teams', _MAX_WORKERS_)
        self.cpu_worktime = params.get('cpu_worktime', _SIMULATION_TIME_)
        self.profiles = params.get('profiles', _PROFILES_)

        # Validate the configuration
        self.validate()

    @classmethod
    def from_ini(cls, file_path=DEFAULT_INI_FILE):
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
            config.num_teams = data.getint('NUM_WORKERS')
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

    def to_ini(self, file_path=DEFAULT_INI_FILE):
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
            task['NUM_WORKERS'] = str(self.num_teams)
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
                    # Convert the list of integers to a string
                    line = ' '.join([str(x) for x in profile])

                    # Write the line to the file
                    file_path.write(f'{line}\n')

            except Exception as e:
                raise BuilderConfigError(
                    info=f"Error writing the profiles section: {e}"
                )

    def validate(self):

        # Check the construction values
        if self.volume_ice_per_foot <= 0:
            raise BuilderConfigError(
                info=f"Invalid volume_ice_per_foot: {self.volume_ice_per_foot}"
            )

        if self.cost_per_volume <= 0:
            raise BuilderConfigError(
                info=f"Invalid cost_per_volume: {self.cost_per_volume}"
            )

        if self.target_height <= 0:
            raise BuilderConfigError(
                info=f"Invalid target_height: {self.target_height}"
            )

        if self.max_section_count <= 0:
            raise BuilderConfigError(
                info=f"Invalid max_section_count: {self.max_section_count}"
            )

        # Check the task values
        if self.num_teams <= 0:
            raise BuilderConfigError(
                info=f"Invalid num_teams: {self.num_teams}"
            )

        if self.cpu_worktime <= 0:
            raise BuilderConfigError(
                info=f"Invalid cpu_worktime: {self.cpu_worktime}"
            )

        # Check the profiles is a two-dimensional list
        if not isinstance(self.profiles, list):
            raise BuilderConfigError(
                info=f"Invalid profiles: {self.profiles}"
            )

        # Check that all elements in the list are integers
        for profile in self.profiles:
            if not isinstance(profile, list):
                raise BuilderConfigError(
                    info=f"Invalid profile: {profile}"
                )

            for value in profile:
                if not isinstance(value, int):
                    raise BuilderConfigError(
                        info=f"Invalid profile value: {value}"
                    )

        # Check the total number of elements in the profiles
        total = sum([len(profile) for profile in self.profiles])
        if total > self.max_section_count:
            raise BuilderConfigError(
                info=f"Total profiles size exceeds max_section_count: {total}"
            )


def main():
    """Main function for testing the configurator."""

    # Read the configuration file
    config = WallConfigurator.from_ini()

    # Print the configuration
    print('Before:')
    print(config)

    # Change the configuration
    before = config.num_teams
    config.num_teams += 1

    # Write the configuration file
    config.to_ini()

    # Read the configuration file again
    config = WallConfigurator.from_ini()
    after = config.num_teams

    # Print the configuration
    print('After:')
    print(config)

    # Compare the new value
    assert (after - before) == 1


if __name__ == "__main__":
    main()
