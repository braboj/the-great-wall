from unittest import TestCase
from builder.configurator import *
import pathlib


class TestConfigurator(TestCase):

    def setUp(self):

        # Create a default configuration file
        self.default_config = WallConfigurator()

        # Define the default profiles
        self.default_config.profiles = [
            [21, 25, 28],
            [17, ],
            [17, 22, 17, 19, 17]
        ]

        # Save the configuration to a file
        self.default_config.to_ini('test.ini')

    def tearDown(self):

        # Delete any ini files
        path = pathlib.Path('test.ini')
        if path.exists():
            path.unlink()

    def test_init(self):

        # Check the default values
        config = WallConfigurator(
            volume_ice_per_foot=1,
            cost_per_volume=2,
            target_height=3,
            max_section_count=4,
            build_rate=5,
            num_teams=6,
            cpu_worktime=7,
            profiles=[1, 2, 3]
        )

        self.assertEqual(config.volume_ice_per_foot, 1)
        self.assertEqual(config.cost_per_volume, 2)
        self.assertEqual(config.target_height, 3)
        self.assertEqual(config.max_section_count, 4)
        self.assertEqual(config.build_rate, 5)
        self.assertEqual(config.num_teams, 6)
        self.assertEqual(config.cpu_worktime, 7)
        self.assertEqual(config.profiles, [1, 2, 3])

    def test_defaults(self):

        # Check the default values
        config = WallConfigurator()
        self.assertEqual(config.volume_ice_per_foot, VOLUME_ICE_PER_FOOT)
        self.assertEqual(config.cost_per_volume, COST_PER_VOLUME)
        self.assertEqual(config.target_height, TARGET_HEIGHT)
        self.assertEqual(config.max_section_count, MAX_SECTION_COUNT)
        self.assertEqual(config.build_rate, BUILD_RATE)
        self.assertEqual(config.num_teams, MAX_WORKERS)
        self.assertEqual(config.cpu_worktime, WORK_DELAY)
        self.assertEqual(config.profiles, PROFILES)

    def test_from_ini(self):

        # Define the default profiles
        expected_profiles = self.default_config.profiles

        # Read the configuration from the default file
        config = WallConfigurator.from_ini('test.ini')

        # Check the configuration
        self.assertEqual(config.volume_ice_per_foot, VOLUME_ICE_PER_FOOT)
        self.assertEqual(config.cost_per_volume, COST_PER_VOLUME)
        self.assertEqual(config.target_height, TARGET_HEIGHT)
        self.assertEqual(config.max_section_count, MAX_SECTION_COUNT)
        self.assertEqual(config.build_rate, BUILD_RATE)
        self.assertEqual(config.num_teams, MAX_WORKERS)
        self.assertEqual(config.cpu_worktime, WORK_DELAY)
        self.assertEqual(config.profiles, expected_profiles)

    def test_to_ini(self):

        # Create a new default configuration
        config = WallConfigurator.from_ini('test.ini')

        # Save the old value
        old_num_workers = config.num_teams

        # Change the number of workers
        config.num_teams += 1

        # Save the configuration to a new file
        config.to_ini('test_modified.ini')

        # Read the configuration from the new file
        config = WallConfigurator.from_ini('test_modified.ini')

        # Check the configuration
        self.assertEqual(config.num_teams, old_num_workers + 1)

        # Delete the test file
        path = pathlib.Path('test_modified.ini')
        path.unlink()
