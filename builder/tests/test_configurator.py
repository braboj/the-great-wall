from unittest import TestCase
from builder.configurator import WallConfigurator
import pathlib


class TestConfigurator(TestCase):

    def test_init(self):

        config = WallConfigurator()
        self.assertEqual(config.volume_ice_per_foot, 195)
        self.assertEqual(config.cost_per_volume, 1900)
        self.assertEqual(config.target_height, 30)
        self.assertEqual(config.max_section_count, 2000)
        self.assertEqual(config.build_rate, 1)
        self.assertEqual(config.num_workers, 20)
        self.assertEqual(config.cpu_worktime, 0.01)
        self.assertEqual(config.profiles, [])
        self.assertEqual(config.log_file, WallConfigurator.LOG_FILE)
        self.assertEqual(config.ini_file, WallConfigurator.INI_FILE)

    def test_from_ini(self):

        # Define the default profiles
        expected_profiles = [
            [21, 25, 28],
            [17, ],
            [17, 22, 17, 19, 17]
        ]

        # Read the configuration from the default file
        config = WallConfigurator.from_ini('test.ini')

        # Check the configuration
        self.assertEqual(config.volume_ice_per_foot, 195)
        self.assertEqual(config.cost_per_volume, 1900)
        self.assertEqual(config.target_height, 30)
        self.assertEqual(config.max_section_count, 2000)
        self.assertEqual(config.build_rate, 1)
        self.assertEqual(config.num_workers, 20)
        self.assertEqual(config.cpu_worktime, 0.01)
        self.assertEqual(config.profiles, expected_profiles)

    def test_to_ini(self):

        # Create a new default configuration
        config = WallConfigurator('test.ini')

        # Save the old value
        old_num_workers = config.num_workers

        # Change the number of workers
        config.num_workers += 1

        # Save the configuration to a new file
        config.to_ini('test.ini')

        # Read the configuration from the new file
        config = WallConfigurator.from_ini('test.ini')

        # Check the configuration
        self.assertEqual(config.num_workers, old_num_workers + 1)

        # Delete the test file
        path = pathlib.Path('test.ini')
        path.unlink()
