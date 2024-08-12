from django.test import TestCase
from django.urls import reverse
import json


class ProfileIndexTests(TestCase):
    """ Test the profile index endpoint."""

    def test_index_status(self):
        """ Test the index endpoint status code."""

        url = reverse('profiles:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class ProfileLogsTests(TestCase):
    """ Test the profile logs endpoint."""

    def test_logs_status(self):
        """ Test the logs endpoint."""
        url = reverse('profiles:get_logs')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class ProfileOverviewTests(TestCase):
    """ Test the profile overview endpoints."""

    def test_overall_overview_status(self):
        """ Test the overall overview endpoint."""

        url = reverse(
            viewname='profiles:get_overall_overview',
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_day_overview_status(self):
        """ Test the day overview endpoint."""

        url = reverse(
            viewname='profiles:get_day_overview',
            kwargs={'day_id': 1}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_profile_overview_status(self):
        """ Test the profile overview endpoint with a valid profile id."""

        url = reverse(
            viewname='profiles:get_profile_overview',
            kwargs={'profile_id': 1, 'day_id': 1}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_invalid_profile_id(self):
        """ Test the profile overview endpoint with an invalid profile id."""

        url = reverse(
            viewname='profiles:get_profile_overview',
            kwargs={'profile_id': 1000, 'day_id': 1}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 500)


class ProfileDailyStatusTests(TestCase):
    """ Test the daily status endpoints."""

    def test_daily_profile_status(self):
        """ Test the daily status endpoint with a valid profile id."""

        url = reverse(
            viewname='profiles:get_day_data',
            kwargs={'profile_id': 1, 'day_id': 1}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_invalid_profile_id(self):
        """ Test the daily status endpoint with an invalid profile id."""

        url = reverse(
            viewname='profiles:get_day_data',
            kwargs={'profile_id': 1000, 'day_id': 1}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 500)


class ProfileConfigTests(TestCase):
    """ Test the configuration endpoints."""

    def test_config_status(self):
        """ Test the configuration endpoint status code."""

        url = reverse('profiles:handle_config')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_config_data(self):
        """ Test the configuration endpoint data."""

        # Get the configuration data
        url = reverse('profiles:handle_config')
        response = self.client.get(url)

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check the response data
        data = json.loads(response.content)
        self.assertIn('volume_ice_per_foot', data)
        self.assertIn('cost_per_volume', data)
        self.assertIn('target_height', data)
        self.assertIn('max_section_count', data)
        self.assertIn('build_rate', data)
        self.assertIn('num_teams', data)
        self.assertIn('cpu_worktime', data)
        self.assertIn('profiles', data)

    def test_config_change(self):
        """ Test changing the configuration data."""

        # Get the configuration data
        url = reverse('profiles:handle_config')

        # Define the data
        expected_data = {
            'status': 'success',
        }

        # Generate the response
        response = self.client.post(
            path=url,
            data=json.dumps(expected_data),
            content_type='application/json'
        )

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check the response data
        obtained_data = json.loads(response.content)
        self.assertEqual(obtained_data, expected_data)

    def test_invalid_config(self):
        """ Test the configuration endpoint with invalid data."""

        # Get the configuration data
        url = reverse('profiles:handle_config')

        # Define the data
        data = {
            'num_teams': -1,
        }

        # Generate the response
        response = self.client.post(
            path=url,
            data=json.dumps(data),
            content_type='application/json'
        )

        # Check the response status code
        self.assertEqual(response.status_code, 400)

        # Set a valid configuration
        data = {
            'num_teams': 20,
        }

        # Generate the response
        self.client.post(
            path=url,
            data=json.dumps(data),
            content_type='application/json'
        )
