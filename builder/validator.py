# encoding: utf-8
from builder.errors import BuilderValidationError
from builder.defines import *
from abc import ABC, abstractmethod


class ConfigValidatorAbc(ABC):

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

    @staticmethod
    def check_primary_key(value):
        """Validates a primary key."""

        # Check the type of section_id
        if not isinstance(value, int):
            raise BuilderValidationError(
                info='The section_id must be an integer'
            )

        # Check that the section_id is positive
        if value < 0:
            raise BuilderValidationError(
                info='The section_id must be a positive integer'
            )

        return True

    @staticmethod
    def check_foreign_key(value):
        """Validates a foreign key."""

        # Check the type of profile_id
        if not isinstance(value, (int, type(None))):
            raise BuilderValidationError(
                info='The profile_id must be an integer'
            )

        # Check that the profile_id is positive
        if value is not None and value < 0:
            raise BuilderValidationError(
                info='The profile_id must be a positive integer'
            )

        return True

    @staticmethod
    def check_iterable(value):
        """Validates an iterable."""

        # Check that the value is an iterable
        if not hasattr(value, '__iter__'):
            raise BuilderValidationError(
                info='The value must be an iterable'
            )

        return True

    @staticmethod
    def check_ice(value):
        """Validates the volume_ice_per_foot parameter."""

        # Check the type of the start height
        if not isinstance(value, int):
            raise BuilderValidationError(
                info='The start height must be an integer'
            )

        # Check that the start height is between 0 and the target height
        if not 0 <= value <= TARGET_HEIGHT:
            raise BuilderValidationError(
                info='The start height must be between 0 and 30'
            )

        return True

    @staticmethod
    def check_cost(value):
        """Validates the cost_per_volume parameter."""

        # Check the type of the start height
        if not isinstance(value, int):
            raise BuilderValidationError(
                info='The start height must be an integer'
            )

        if value <= 0:
            raise BuilderValidationError(
                info=f"Invalid value for cost_per_volume: {value}"
            )

        return True

    @staticmethod
    def check_height(value):
        """Validates the target_height parameter."""

        # Check the type of the start height
        if not isinstance(value, int):
            raise BuilderValidationError(
                info='The start height must be an integer'
            )

        if not 0 <= value <= TARGET_HEIGHT:
            raise BuilderValidationError(
                info=f"Invalid value for target_height: {value}"
            )

        return True

    @staticmethod
    def check_section_count(value):
        """Validates the max_section_count parameter."""

        # Check the type of the value
        if not isinstance(value, int):
            raise BuilderValidationError(
                info='The start height must be an integer'
            )

        if not value < 0 < MAX_SECTION_COUNT:
            raise BuilderValidationError(
                info=f"Invalid value for max_section_count: {value}"
            )

        return True

    @staticmethod
    def check_build_rate(value):
        """Validates the build_rate parameter."""

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
        """Validates the num_teams parameter."""

        if not isinstance(value, int):
            raise BuilderValidationError(
                info=f"Invalid num_teams: {value}. Allowed up to {MAX_WORKERS}"
            )

        if not 0 < value < MAX_WORKERS:
            raise BuilderValidationError(
                info=f"Invalid num_teams: {value}. Allowed up to {MAX_WORKERS}"
            )

        return True

    @staticmethod
    def check_cpu_worktime(value):
        """Validates the cpu_worktime parameter."""

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
        """Validates the sections parameter."""

        # Check the sections is an iterable
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
        """Validates the profiles parameter."""

        # Check the profiles is an iterable
        if not hasattr(value, '__iter__'):
            raise BuilderValidationError(
                info='The profiles must be an iterable'
            )

        # Check the total amount of elements
        total = sum(1 for _ in value)
        if not 0 < total < MAX_SECTION_COUNT:
            raise BuilderValidationError(
                info='The profiles list cannot be empty'
            )

        return True

    @staticmethod
    def check_config_list(value):
        """Validates the profile list."""

        # Check the profiles is an iterable
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

        # Check the total amount of elements
        total = sum(len(x) for x in value)
        if not 0 < total < MAX_SECTION_COUNT:
            raise BuilderValidationError(
                info='The profiles list cannot be empty'
            )

        return True
