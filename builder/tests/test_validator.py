from unittest import TestCase
from builder.validator import ConfigValidator
from builder.errors import *
from builder.defines import *


class TestConfigValidator(TestCase):

    def setUp(self):
        self.validator = ConfigValidator()

    def test_check_primary_key(self):

        self.assertTrue(self.validator.check_primary_key(1))
        self.assertTrue(self.validator.check_primary_key(100))
        self.assertTrue(self.validator.check_primary_key(0))

        with self.assertRaises(BuilderValidationError):
            self.validator.check_primary_key(-1)

        with self.assertRaises(BuilderValidationError):
            self.validator.check_primary_key("1")

        with self.assertRaises(BuilderValidationError):
            self.validator.check_primary_key(1.0)

    def test_check_foreign_key(self):
        self.assertTrue(self.validator.check_foreign_key(1))
        self.assertTrue(self.validator.check_foreign_key(100))
        self.assertTrue(self.validator.check_foreign_key(0))

        with self.assertRaises(BuilderValidationError):
            self.validator.check_foreign_key(-1)

        with self.assertRaises(BuilderValidationError):
            self.validator.check_foreign_key("1")

        with self.assertRaises(BuilderValidationError):
            self.validator.check_foreign_key(1.0)

    def test_check_iterable(self):
        self.assertTrue(self.validator.check_iterable([1, 2, 3]))
        self.assertTrue(self.validator.check_iterable([1]))
        self.assertTrue(self.validator.check_iterable([]))

        with self.assertRaises(BuilderValidationError):
            self.validator.check_iterable(1)

        with self.assertRaises(BuilderValidationError):
            self.validator.check_iterable(1.0)

    def test_check_ice(self):
        self.assertTrue(self.validator.check_ice(10))
        self.assertTrue(self.validator.check_ice(100))

        with self.assertRaises(BuilderValidationError):
            self.validator.check_ice(0)

        with self.assertRaises(BuilderValidationError):
            self.validator.check_ice(-1)

        with self.assertRaises(BuilderValidationError):
            self.validator.check_ice("1")

        with self.assertRaises(BuilderValidationError):
            self.validator.check_ice(1.0)

    def test_check_cost(self):

        self.assertTrue(self.validator.check_cost(1))
        self.assertTrue(self.validator.check_cost(1000))

        with self.assertRaises(BuilderValidationError):
            self.validator.check_cost(0)

        with self.assertRaises(BuilderValidationError):
            self.validator.check_cost(-1)

        with self.assertRaises(BuilderValidationError):
            self.validator.check_cost("1")

        with self.assertRaises(BuilderValidationError):
            self.validator.check_cost(1.0)

    def test_check_height(self):

        self.assertTrue(self.validator.check_height(0))
        self.assertTrue(self.validator.check_height(1))
        self.assertTrue(self.validator.check_height(30))

        with self.assertRaises(BuilderValidationError):
            self.validator.check_height(-1)

        with self.assertRaises(BuilderValidationError):
            self.validator.check_height("1")

        with self.assertRaises(BuilderValidationError):
            self.validator.check_height(1.0)

    def test_check_section_count(self):

        self.assertTrue(self.validator.check_section_count(1))
        self.assertTrue(self.validator.check_section_count(1999))

        with self.assertRaises(BuilderValidationError):
            self.validator.check_section_count(0)

        with self.assertRaises(BuilderValidationError):
            self.validator.check_section_count(-1)

        with self.assertRaises(BuilderValidationError):
            self.validator.check_section_count("1")

        with self.assertRaises(BuilderValidationError):
            self.validator.check_section_count(1.0)

    def test_check_build_rate(self):

        self.assertTrue(self.validator.check_build_rate(1))
        self.assertTrue(self.validator.check_build_rate(1000))

        with self.assertRaises(BuilderValidationError):
            self.validator.check_build_rate(0)

        with self.assertRaises(BuilderValidationError):
            self.validator.check_build_rate(-1)

        with self.assertRaises(BuilderValidationError):
            self.validator.check_build_rate("1")

        with self.assertRaises(BuilderValidationError):
            self.validator.check_build_rate(1.0)

    def test_check_num_teams(self):

        self.assertTrue(self.validator.check_num_teams(1))
        self.assertTrue(self.validator.check_num_teams(20))

        with self.assertRaises(BuilderValidationError):
            self.validator.check_num_teams(0)

        with self.assertRaises(BuilderValidationError):
            self.validator.check_num_teams(30)

        with self.assertRaises(BuilderValidationError):
            self.validator.check_num_teams(-1)

        with self.assertRaises(BuilderValidationError):
            self.validator.check_num_teams("1")

        with self.assertRaises(BuilderValidationError):
            self.validator.check_num_teams(1.0)

    def test_check_cpu_worktime(self):

        self.assertTrue(self.validator.check_cpu_worktime(0.01))
        self.assertTrue(self.validator.check_cpu_worktime(1.0))

        with self.assertRaises(BuilderValidationError):
            self.validator.check_cpu_worktime(0)

        with self.assertRaises(BuilderValidationError):
            self.validator.check_cpu_worktime(-1)

        with self.assertRaises(BuilderValidationError):
            self.validator.check_cpu_worktime("1")

        with self.assertRaises(BuilderValidationError):
            self.validator.check_cpu_worktime(1)

    def test_check_sections(self):

        self.assertTrue(self.validator.check_sections([1, 2, 3]))
        self.assertTrue(self.validator.check_sections([1]))

        with self.assertRaises(BuilderValidationError):
            self.validator.check_sections([])

        with self.assertRaises(BuilderValidationError):
            self.validator.check_sections(1)

        with self.assertRaises(BuilderValidationError):
            self.validator.check_sections(1.0)

        with self.assertRaises(BuilderValidationError):
            self.validator.check_config_list([[1,] * 2000])

    def test_check_profiles(self):

        self.assertTrue(self.validator.check_profiles([1, 2, 3]))
        self.assertTrue(self.validator.check_profiles([1]))

        with self.assertRaises(BuilderValidationError):
            self.validator.check_profiles([])

        with self.assertRaises(BuilderValidationError):
            self.validator.check_profiles(1)

        with self.assertRaises(BuilderValidationError):
            self.validator.check_profiles(1.0)

        with self.assertRaises(BuilderValidationError):
            self.validator.check_config_list([[1,] * 2000])

    def test_check_config_list(self):

        self.assertTrue(self.validator.check_config_list([[1], [1, 2,]]))

        with self.assertRaises(BuilderValidationError):
            self.validator.check_config_list([])

        with self.assertRaises(BuilderValidationError):
            self.validator.check_config_list([[1], ['1']])

        with self.assertRaises(BuilderValidationError):
            self.validator.check_config_list(1)

        with self.assertRaises(BuilderValidationError):
            self.validator.check_config_list(1.0)

        with self.assertRaises(BuilderValidationError):
            self.validator.check_config_list([[1], [2,] * 2000])