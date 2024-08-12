# encoding: utf-8
from builder.errors import BuilderValidationError
from builder.defines import *
from abc import ABC, abstractmethod


class ConfigValidatorAbc(ABC):
    """Abstract class for validating builder configuration parameters."""

    @abstractmethod
    def check_primary_key(self, value):
        pass

    @abstractmethod
    def check_foreign_key(self, value):
        pass

    @abstractmethod
    def check_iterable(self, value):
        pass

    @abstractmethod
    def check_ice(self, value):
        pass

    @abstractmethod
    def check_cost(self, value):
        pass

    @abstractmethod
    def check_height(self, value):
        pass

    @abstractmethod
    def check_section_count(self, value):
        pass

    @abstractmethod
    def check_build_rate(self, value):
        pass

    @abstractmethod
    def check_num_teams(self, value):
        pass

    @abstractmethod
    def check_cpu_worktime(self, value):
        pass

    @abstractmethod
    def check_sections(self, value):
        pass

    @abstractmethod
    def check_profiles(self, value):
        pass

    @abstractmethod
    def check_config_list(self, value):
        pass


class ConfigValidator(object):
    """Class for validating builder configuration parameters.

    Example:
        >>> validator = ConfigValidator()
        >>> validator.check_primary_key(1)
        True
        >>> validator.check_foreign_key(1)
        True
        >>> validator.check_iterable([1, 2, 3])
        True
        >>> validator.check_ice(10)
        True
        >>> validator.check_cost(100)
        True
        >>> validator.check_height(30)
        True
        >>> validator.check_section_count(100)
        True
        >>> validator.check_build_rate(1)
        True
        >>> validator.check_num_teams(1)
        True
        >>> validator.check_cpu_worktime(0.01)
        True
        >>> validator.check_sections([1, 2, 3])
        True
        >>> validator.check_profiles([1, 2, 3])
        True
        >>> validator.check_config_list([[1, 2, 3], [4, 5, 6]])
        True

    """

    @staticmethod
    def check_primary_key(value):
        """Checks the primary key."""

        # Check the type of the value
        if not isinstance(value, int):
            raise BuilderValidationError(
                info='The primary key must be an integer'
            )

        # Check that the value is positive
        if value < 0:
            raise BuilderValidationError(
                info='The primary key must be a positive integer'
            )

        return True

    @staticmethod
    def check_foreign_key(value):
        """Checks a foreign key."""

        # Check the type of the value
        if not isinstance(value, (int, type(None))):
            raise BuilderValidationError(
                info='The foreign key must be an integer'
            )

        # Check that the value is positive or None
        if value is not None and value < 0:
            raise BuilderValidationError(
                info='The foreign key must be a positive integer'
            )

        return True

    @staticmethod
    def check_iterable(value):
        """Checks if iterable."""

        # Check that the value is iterable
        if not hasattr(value, '__iter__'):
            raise BuilderValidationError(
                info='The provided value must be an iterable'
            )

        return True

    @staticmethod
    def check_ice(value):
        """Checks a volume_ice_per_foot parameter."""

        # Check the type of the value
        if not isinstance(value, int):
            raise BuilderValidationError(
                info='The ice volume must be an integer'
            )

        # Check that the value is positive
        if value <= 0:
            raise BuilderValidationError(
                info='The ice volume must be a positive integer'
            )

        return True

    @staticmethod
    def check_cost(value):
        """Checks a cost_per_volume parameter."""

        # Check the type of the value
        if not isinstance(value, int):
            raise BuilderValidationError(
                info='The material cost must be an integer'
            )

        # Check if the value is positive
        if value <= 0:
            raise BuilderValidationError(
                info=f"The material cost must be a positive integer: {value}"
            )

        return True

    @staticmethod
    def check_height(value):
        """Checks a target_height parameter."""

        # Check the type of the value
        if not isinstance(value, int):
            raise BuilderValidationError(
                info='The start height must be an integer'
            )

        # Check that the value is within the allowed range
        if not 0 <= value <= TARGET_HEIGHT:
            raise BuilderValidationError(
                info=f"Invalid value for target_height: {value}"
            )

        return True

    @staticmethod
    def check_section_count(value):
        """Checks a max_section_count parameter."""

        # Check the type of the value
        if not isinstance(value, int):
            raise BuilderValidationError(
                info='The start height must be an integer'
            )

        # Check that the value is within the allowed range
        if not 0 < value < MAX_SECTION_COUNT:
            raise BuilderValidationError(
                info=f"Invalid value for max_section_count: {value}"
            )

        return True

    @staticmethod
    def check_build_rate(value):
        """Checks a build_rate parameter."""

        # Check the type of the value
        if not isinstance(value, int):
            raise BuilderValidationError(
                info='The start height must be an integer'
            )

        # Check that the value is positive
        if value <= 0:
            raise BuilderValidationError(
                info=f"Invalid value for build_rate: {value}"
            )

        return True

    @staticmethod
    def check_num_teams(value):
        """Checks a num_teams parameter."""

        # Check the type of the value
        if not isinstance(value, int):
            raise BuilderValidationError(
                info=f"Invalid num_teams: {value}. Allowed up to {MAX_WORKERS}"
            )

        # Check that the value is within the allowed range
        if not 0 < value <= MAX_WORKERS:
            raise BuilderValidationError(
                info=f"Invalid num_teams: {value}. Allowed up to {MAX_WORKERS}"
            )

        return True

    @staticmethod
    def check_cpu_worktime(value):
        """Checks a cpu_worktime parameter."""

        # Check the type of the value
        if not isinstance(value, float):
            raise BuilderValidationError(
                info='The start height must be a float'
            )

        # Check that the value is positive
        if value <= 0:
            raise BuilderValidationError(
                info=f"Invalid value for cpu_worktime: {value}"
            )

        return True

    @staticmethod
    def check_sections(value):
        """Checks a section parameter."""

        # Check the sections is iterable
        if not hasattr(value, '__iter__'):
            raise BuilderValidationError(
                info='The sections must be an iterable'
            )

        # Count the total number of elements
        total = sum(1 for _ in value)
        if not 0 < total < MAX_SECTION_COUNT:
            raise BuilderValidationError(
                info='The sections list cannot be empty'
            )

        return True

    @staticmethod
    def check_profiles(value):
        """Checks a profile parameter."""

        # Check the profiles is iterable
        if not hasattr(value, '__iter__'):
            raise BuilderValidationError(
                info='The profiles must be an iterable'
            )

        # Check the total number of elements
        total = sum(1 for _ in value)
        if not 0 < total < MAX_SECTION_COUNT:
            raise BuilderValidationError(
                info='The profiles list cannot be empty'
            )

        return True

    @staticmethod
    def check_config_list(value):
        """Checks a profile configuration list."""

        # Check the profiles is iterable
        if not hasattr(value, '__iter__'):
            raise BuilderValidationError(
                info='The profiles must be an iterable'
            )

        # Check if the list is two-dimensional
        if not all(isinstance(x, list) for x in value):
            raise BuilderValidationError(
                info='The profiles must be a two-dimensional list'
            )

        # Check that all elements are integers
        for element in value:
            if not all(isinstance(x, int) for x in element):
                raise BuilderValidationError(
                    info='The profiles must contain only integers'
                )

        # Check the total number of elements
        total = sum(len(x) for x in value)
        if not 0 < total < MAX_SECTION_COUNT:
            raise BuilderValidationError(
                info='The profiles list cannot be empty'
            )

        return True
