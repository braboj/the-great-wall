from django.test import TestCase
from .builder import *


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
        for i in range(TARGET_HEIGHT):
            self.section.build()

        # Check the section is ready
        self.assertTrue(self.section.is_ready())

    def test_build(self):

        # Build and check the height is incremented
        for i in range(TARGET_HEIGHT):
            self.section.build()

        # Check the current height is equal to the target height
        self.assertEqual(self.section.current_height, TARGET_HEIGHT)

    def test_get_ice(self):

        # Initialize the start height
        self.section.start_height = 0

        # Check the total ice is zero
        self.assertEqual(self.section.get_ice(), 0)

        # Build one foot of ice
        self.section.build()

        # Check the total ice is one foot * VOLUME_ICE_PER_FOOT
        self.assertEqual(self.section.get_ice(), VOLUME_ICE_PER_FOOT)

        # Build until the target height is reached
        for i in range(TARGET_HEIGHT):
            self.section.build()

        # ICE = (TARGET_HEIGHT - START_HEIGHT) * VOLUME_ICE_PER_FOOT
        difference = TARGET_HEIGHT - self.section.start_height
        expected_ice = difference * VOLUME_ICE_PER_FOOT
        self.assertEqual(self.section.get_ice(), expected_ice)

    def test_get_cost(self):

        # Initialize the start height
        self.section.start_height = 0

        # Check the total cost is zero
        self.assertEqual(self.section.get_cost(), 0)

        # Build one foot of ice
        self.section.build()

        # ICE = (TARGET_HEIGHT - START_HEIGHT) * VOLUME_ICE_PER_FOOT
        # COST = ICE * COST_PER_VOLUME
        expected_cost = VOLUME_ICE_PER_FOOT * COST_PER_VOLUME
        self.assertEqual(self.section.get_cost(), expected_cost)

        # Build until the target height is reached
        for i in range(TARGET_HEIGHT):
            self.section.build()

        # ICE = (TARGET_HEIGHT - START_HEIGHT) * VOLUME_ICE_PER_FOOT
        delta = TARGET_HEIGHT - self.section.start_height
        expected_ice = delta * VOLUME_ICE_PER_FOOT
        expected_cost = expected_ice * COST_PER_VOLUME
        self.assertEqual(self.section.get_cost(), expected_cost)

    def test_validate(self):

        # Set the start height to valid values
        self.section.start_height = 0
        test_values = [0, TARGET_HEIGHT]
        for value in test_values:
            self.section.start_height = value
            self.section.validate()

        # Set the start height to invalid types
        self.section.start_height = 0
        test_values = [None, 'a', 1.0, complex(1, 1)]
        for value in test_values:
            with self.assertRaises(TypeError):
                self.section.start_height = value
                self.section.validate()

        # Set the start height to invalid values
        self.section.start_height = 0
        test_values = [-1, TARGET_HEIGHT + 1]
        for value in test_values:
            with self.assertRaises(ValueError):
                self.section.start_height = value
                self.section.validate()

        # Set the name to valid values
        self.section.start_height = 0
        test_values = ['a', 'a' * 100]
        for value in test_values:
            self.section.name = value
            self.section.validate()

        # Set the name to invalid types
        self.section.start_height = 0
        test_values = [None, 1, 1.0, complex(1, 1)]
        for value in test_values:
            with self.assertRaises(TypeError):
                self.section.name = value
                self.section.validate()


class TestWallProfile(TestCase):

    def setUp(self):
        self.sections = [WallSection(i) for i in range(3)]
        self.profile = WallProfile(self.sections)

    def test_init(self):

        # Check the sections are set
        self.assertEqual(self.profile.sections, self.sections)

        # Check the name is set
        self.assertEqual(self.profile.name, '')

    def test_is_ready(self):

        # Initialize the start height
        for section in self.sections:
            section.start_height = 0

        # Check the profile is not ready
        self.assertFalse(self.profile.is_ready())

        # Build until the target height is reached
        for section in self.sections:
            for i in range(TARGET_HEIGHT):
                section.build()

        # Check the profile is ready
        self.assertTrue(self.profile.is_ready())

    def test_get_ice(self):

        # Check the total ice is zero
        self.assertEqual(self.profile.get_ice(), 0)

        # Build one foot of ice
        for section in self.sections:
            section.build()

        # Check the total ice is one foot * VOLUME_ICE_PER_FOOT
        expected_ice = VOLUME_ICE_PER_FOOT * len(self.sections)
        self.assertEqual(self.profile.get_ice(), expected_ice)

        # Build until the target height is reached
        for section in self.sections:
            for i in range(TARGET_HEIGHT):
                section.build()

        # ICE = sum((TARGET_HEIGHT - START_HEIGHT) * VOLUME_ICE_PER_FOOT)
        expected_ice = sum(
            (TARGET_HEIGHT - section.start_height) * VOLUME_ICE_PER_FOOT for
            section in self.sections
        )
        self.assertEqual(self.profile.get_ice(), expected_ice)

    def test_get_cost(self):

        # Check the total cost is zero
        self.assertEqual(self.profile.get_cost(), 0)

        # Build until the target height is reached
        for section in self.sections:
            for i in range(TARGET_HEIGHT):
                section.build()

        # ICE = sum((TARGET_HEIGHT - START_HEIGHT) * VOLUME_ICE_PER_FOOT)
        # COST = ICE * COST_PER_VOLUME
        expected_ice = sum(
            (TARGET_HEIGHT - section.start_height) * VOLUME_ICE_PER_FOOT for
            section in self.sections
        )
        expected_cost = expected_ice * COST_PER_VOLUME
        self.assertEqual(self.profile.get_cost(), expected_cost)

    def test_build(self):

        # Check the profile is not ready
        self.assertFalse(self.profile.is_ready())

        # Build and check the height is incremented
        for section in self.sections:
            for i in range(TARGET_HEIGHT):
                section.build()

        # Check the profile is ready
        self.assertTrue(self.profile.is_ready())

        # Check that the current height is equal to the target height
        for section in self.sections:
            self.assertEqual(section.current_height, TARGET_HEIGHT)

    def test_validate(self):

        # Set the name to valid values
        profile = WallProfile(self.sections)
        test_values = ['a', 'a' * 100]
        for value in test_values:
            profile.name = value
            profile.validate()

        # Set the name to invalid types
        profile = WallProfile(self.sections)
        test_values = [None, 1, 1.0, complex(1, 1)]
        for value in test_values:
            with self.assertRaises(TypeError):
                profile.name = value
                profile.validate()

        # Set the sections to valid values
        profile = WallProfile(self.sections)
        test_values = [[WallSection(0)], [WallSection(0), WallSection(1)]]
        for value in test_values:
            profile.sections = value
            profile.validate()

        # Set the sections to invalid types
        profile = WallProfile(self.sections)
        test_values = [None, 1, 1.0, complex(1, 1)]
        for value in test_values:
            with self.assertRaises(TypeError):
                profile.sections = value
                profile.validate()

        # Set the sections to invalid size
        profile = WallProfile(self.sections)
        test_values = [[], [WallSection(0)] * (MAX_SECTION_COUNT + 1)]
        for value in test_values:
            with self.assertRaises(MemoryError):
                profile.sections = value
                profile.validate()


class TestWallBuilder(TestCase):

    def setUp(self):
        self.builder = WallBuilder()
        self.sections = [WallSection(i) for i in range(3)]
        self.profiles = [WallProfile(self.sections) for _ in range(3)]
        self.builder.wall_profiles = self.profiles

    def test_init(self):

        # Check the config list is set
        self.assertEqual(self.builder.config_list, [])

        # Check the wall profiles are set
        self.assertEqual(self.builder.wall_profiles, self.profiles)

        # Check the sections are set
        self.assertEqual(self.builder.sections, [])

        # Check the logger is set
        self.assertIsNotNone(self.builder.log)

    def test_create_profile(self):

        # Create a profile
        heights = [0, 1, 2]
        profile = WallBuilder.create_profile(heights, 0)

        # Check the profile is created
        self.assertEqual(profile.name, 'P00')
        self.assertEqual(profile.sections[0].start_height, 0)
        self.assertEqual(profile.sections[1].start_height, 1)
        self.assertEqual(profile.sections[2].start_height, 2)

    def test_set_config(self):

        # Set the config list
        config_list = [1, 2, 3]
        self.builder.set_config(config_list)

        # Check the config list is set
        self.assertEqual(self.builder.config_list, config_list)

    def test_get_sections(self):

        # Check the sections are returned
        self.assertEqual(self.builder.get_sections(), self.sections)

    def test_is_ready(self):

        # Check the builder is not ready
        self.assertFalse(self.builder.is_ready())

        # Build until the target height is reached
        for profile in self.profiles:
            for section in profile.sections:
                for i in range(TARGET_HEIGHT):
                    section.build()

        # Check the builder is ready
        self.assertTrue(self.builder.is_ready())
