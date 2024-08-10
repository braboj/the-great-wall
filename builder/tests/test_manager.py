from unittest import TestCase
from builder.manager import *
from builder.errors import *
from builder.configurator import (
    _TARGET_HEIGHT_,
    _VOLUME_ICE_PER_FOOT_,
    _COST_PER_VOLUME_,
    _MAX_SECTION_COUNT_
)


class TestWallSection(TestCase):

    def setUp(self):
        self.section = WallSection(0)

    def test_init(self):

        # Check the start height is set
        self.assertEqual(self.section.start_height, 0)
        self.assertEqual(self.section.current_height, 0)

    def test_is_ready(self):

        # Initialize the start height
        self.section.start_height = 0

        # Check the section is not ready
        self.assertFalse(self.section.is_ready())

        # Build until the target height is reached
        for i in range(_TARGET_HEIGHT_):
            self.section.build()

        # Check the section is ready
        self.assertTrue(self.section.is_ready())

    def test_build(self):

        # Build and check the height is incremented
        for i in range(_TARGET_HEIGHT_):
            self.section.build()

        # Check the current height is equal to the target height
        self.assertEqual(self.section.current_height, _TARGET_HEIGHT_)

    def test_get_ice(self):

        # Initialize the start height
        self.section.start_height = 0

        # Check the total ice is zero
        self.assertEqual(self.section.get_ice(), 0)

        # Build one foot of ice
        self.section.build()

        # Check the total ice is one foot * _VOLUME_ICE_PER_FOOT_
        self.assertEqual(self.section.get_ice(), _VOLUME_ICE_PER_FOOT_)

        # Build until the target height is reached
        for i in range(_TARGET_HEIGHT_):
            self.section.build()

        # ICE = (_TARGET_HEIGHT_ - START_HEIGHT) * _VOLUME_ICE_PER_FOOT_
        difference = _TARGET_HEIGHT_ - self.section.start_height
        expected_ice = difference * _VOLUME_ICE_PER_FOOT_
        self.assertEqual(self.section.get_ice(), expected_ice)

    def test_get_cost(self):

        # Initialize the start height
        self.section.start_height = 0

        # Check the total cost is zero
        self.assertEqual(self.section.get_cost(), 0)

        # Build one foot of ice
        self.section.build()

        # ICE = (_TARGET_HEIGHT_ - START_HEIGHT) * _VOLUME_ICE_PER_FOOT_
        # COST = ICE * _COST_PER_VOLUME_
        expected_cost = _VOLUME_ICE_PER_FOOT_ * _COST_PER_VOLUME_
        self.assertEqual(self.section.get_cost(), expected_cost)

        # Build until the target height is reached
        for i in range(_TARGET_HEIGHT_):
            self.section.build()

        # ICE = (_TARGET_HEIGHT_ - START_HEIGHT) * _VOLUME_ICE_PER_FOOT_
        delta = _TARGET_HEIGHT_ - self.section.start_height
        expected_ice = delta * _VOLUME_ICE_PER_FOOT_
        expected_cost = expected_ice * _COST_PER_VOLUME_
        self.assertEqual(self.section.get_cost(), expected_cost)

    def test_validate_start_height(self):

        # ---------------------------------------------------------------------
        # Test the validation of the start height

        # Set the start height to valid values
        section = WallSection(section_id=1, start_height=0)
        test_values = [0, _TARGET_HEIGHT_]
        for value in test_values:
            section.start_height = value
            section.validate()

        # Set the start height to invalid types
        section = WallSection(section_id=1, start_height=0)
        test_values = [None, 'a', -1, 31, 1.0, complex(1, 1)]
        for value in test_values:
            with self.assertRaises(BuilderValidationError):
                section.start_height = value
                section.validate()

    def test_validate_section_id(self):

        # ---------------------------------------------------------------------
        # Test the validation of the section-id

        # Set the section-id to valid values
        section = WallSection(section_id=1, start_height=0)
        test_values = [0, 1, 2, 3]
        for value in test_values:
            section.section_id = value
            section.validate()

        # Set the section-id to invalid values
        section = WallSection(section_id=1, start_height=0)
        test_values = [None, -1, 'a', 1.0, complex(1, 1)]
        for value in test_values:
            with self.assertRaises(BuilderValidationError):
                section.section_id = value
                section.validate()

    def test_validate_profile_id(self):

        # ---------------------------------------------------------------------
        # Test the validation of the profile-id

        # Set the section-id to valid values
        section = WallSection(section_id=1, start_height=0)
        test_values = [None, 0, 1]
        for value in test_values:
            section.profile_id = value
            section.validate()

        # Set the section-id to invalid values
        section = WallSection(section_id=1, start_height=0)
        test_values = ['a', -1, 1.0, complex(1, 1)]
        for value in test_values:
            with self.assertRaises(BuilderValidationError):
                section.profile_id = value
                section.validate()


class TestWallProfile(TestCase):

    def setUp(self):
        self.sections = [WallSection(i) for i in range(3)]
        self.profile = WallProfile(profile_id=1, sections=self.sections)

    def test_init(self):

        # Check the sections are set
        self.assertEqual(self.profile.sections, self.sections)

        # Check the name is set
        self.assertEqual(self.profile.profile_id, 1)

    def test_is_ready(self):

        # Initialize the start height
        for section in self.sections:
            section.start_height = 0

        # Check the profile is not ready
        self.assertFalse(self.profile.is_ready())

        # Build until the target height is reached
        for section in self.sections:
            for i in range(_TARGET_HEIGHT_):
                section.build()

        # Check the profile is ready
        self.assertTrue(self.profile.is_ready())

    def test_get_ice(self):

        # Check the total ice is zero
        self.assertEqual(self.profile.get_ice(), 0)

        # Build one foot of ice
        for section in self.sections:
            section.build()

        # Check the total ice is one foot * _VOLUME_ICE_PER_FOOT_
        expected_ice = _VOLUME_ICE_PER_FOOT_ * len(self.sections)
        self.assertEqual(self.profile.get_ice(), expected_ice)

        # Build until the target height is reached
        for section in self.sections:
            for i in range(_TARGET_HEIGHT_):
                section.build()

        # ICE = sum((_TARGET_HEIGHT_ - START_HEIGHT) * _VOLUME_ICE_PER_FOOT_)
        expected_ice = sum(
            (_TARGET_HEIGHT_ - section.start_height) * _VOLUME_ICE_PER_FOOT_ for
            section in self.sections
        )
        self.assertEqual(self.profile.get_ice(), expected_ice)

    def test_get_cost(self):

        # Check the total cost is zero
        self.assertEqual(self.profile.get_cost(), 0)

        # Build until the target height is reached
        for section in self.sections:
            for i in range(_TARGET_HEIGHT_):
                section.build()

        # ICE = sum((_TARGET_HEIGHT_ - START_HEIGHT) * _VOLUME_ICE_PER_FOOT_)
        # COST = ICE * _COST_PER_VOLUME_
        expected_ice = sum(
            (_TARGET_HEIGHT_ - section.start_height) * _VOLUME_ICE_PER_FOOT_ for
            section in self.sections
        )
        expected_cost = expected_ice * _COST_PER_VOLUME_
        self.assertEqual(self.profile.get_cost(), expected_cost)

    def test_build(self):

        # Check the profile is not ready
        self.assertFalse(self.profile.is_ready())

        # Build and check the height is incremented
        for section in self.sections:
            for i in range(_TARGET_HEIGHT_):
                section.build()

        # Check the profile is ready
        self.assertTrue(self.profile.is_ready())

        # Check that the current height is equal to the target height
        for section in self.sections:
            self.assertEqual(section.current_height, _TARGET_HEIGHT_)

    def test_validate_profile_id(self):

        # Set the profile-id to valid values
        profile = WallProfile(profile_id=1, sections=self.sections)
        test_values = [0, 1]
        for value in test_values:
            profile.name = value
            profile.validate()

        # Set the profile-id to invalid types
        profile = WallProfile(profile_id=1, sections=self.sections)
        test_values = [None, 'a', -1, 1.0, complex(1, 1)]
        for value in test_values:
            with self.assertRaises(BuilderValidationError):
                profile.profile_id = value
                profile.validate()

    def test_validate_sections(self):

        # Set the sections to valid values
        profile = WallProfile(profile_id=1, sections=self.sections)
        test_values = [[WallSection(0)], [WallSection(0), WallSection(1)]]
        for value in test_values:
            profile.sections = value
            profile.validate()

        # Set the sections to invalid types
        profile = WallProfile(profile_id=1, sections=self.sections)
        test_values = [None, 1, 1.0, complex(1, 1)]
        for value in test_values:
            with self.assertRaises(BuilderValidationError):
                profile.sections = value
                profile.validate()

        # Set the sections to invalid size
        profile = WallProfile(profile_id=1, sections=self.sections)
        test_values = [[], [WallSection(0)] * (_MAX_SECTION_COUNT_ + 1)]
        for value in test_values:
            with self.assertRaises(BuilderValidationError):
                profile.sections = value
                profile.validate()


class TestWallManager(TestCase):

    def test_init(self):

        config_list = [[1, ], [4, ]]
        manager = WallManager(config_list)

        # Check the config list is set
        self.assertEqual(manager.config_list, config_list)

    def test_is_ready(self):

        # Define the config list
        config_list = [[1, 2], [3, ]]

        # Initialize the manager
        manager = WallManager(config_list)

        # Check the manager is not ready
        self.assertFalse(manager.is_ready())

        # Build until the target height is reached
        manager.build(days=30)

        # Check the manager is ready
        self.assertTrue(manager.is_ready())

    def test_get_ice(self):

        # Define the config list
        config_list = [[29, 29], [29, ]]

        # Define the expected result
        expected_ice = 3 * (_TARGET_HEIGHT_ - 29) * _VOLUME_ICE_PER_FOOT_

        # Create the manager
        manager = WallManager(config_list)

        # Build for one day
        manager.build(days=1)

        # Check the total ice is correct
        self.assertEqual(manager.get_ice(), expected_ice)

    def test_get_cost(self):

        # Define the config list
        config_list = [[29, 29], [29, ]]

        # Define the expected result
        expected_cost = (3 * (_TARGET_HEIGHT_ - 29) *
                         _VOLUME_ICE_PER_FOOT_ *
                         _COST_PER_VOLUME_
                         )

        # Create the manager
        manager = WallManager(config_list)

        # Build for one day
        manager.build(days=1)

        # Check the total cost is correct
        self.assertEqual(manager.get_cost(), expected_cost)

    def test_build(self):

        # Define the config list
        config_list = [[29, 29], [29, ]]

        # Initialize the manager
        manager = WallManager(config_list)

        # Build for one day
        manager.build(days=1)

        # Check the manager is ready
        self.assertTrue(manager.is_ready())

    def test_validate_config_list(self):

        # Create the manager
        manager = WallManager([])

        # Define a valid nested list
        manager.config_list = [[1, 2], [3, 4]]
        manager.validate()

        # Check the validation fails
        config_list = [1, 2, 3, 4, 5]
        with self.assertRaises(BuilderValidationError):
            manager.config_list = config_list
            manager.validate()

        # Define an invalid list with non-integer values
        config_list = [[1, 2], [3, 'a']]
        with self.assertRaises(BuilderValidationError):
            manager.config_list = config_list
            manager.validate()
