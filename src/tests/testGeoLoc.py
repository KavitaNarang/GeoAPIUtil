import unittest
import click
from click.testing import CliRunner
from src.geoLoc import geoloc_util

class TestGeoLocUtil(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_single_city_state(self):
        result = self.runner.invoke(geoloc_util, ['--locations', 'Madison, WI'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Location: Madison, WI', result.output)
        self.assertIn('Name: Madison', result.output)
        self.assertIn('State: Wisconsin', result.output)
        self.assertIn('Country: US', result.output)
        self.assertIn('Latitude', result.output)
        self.assertIn('Longitude', result.output)

    def test_single_zip_code(self):
        result = self.runner.invoke(geoloc_util, ['--locations', '94401'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Name: San Mateo', result.output)
        self.assertIn('Country: US', result.output)
        self.assertIn('Latitude', result.output)
        self.assertIn('Longitude', result.output)
        self.assertIn('Zip: 94401', result.output)

    def test_valid_zip_code(self):
        result = self.runner.invoke(geoloc_util, ['10001'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Name: New York', result.output)
        self.assertIn('Country: US', result.output)
        self.assertIn('Latitude', result.output)
        self.assertIn('Longitude', result.output)
        self.assertIn('Zip: 10001', result.output)
    
    def test_multiple_locations(self):
        result = self.runner.invoke(geoloc_util, ['--locations', 'Chicago, IL', '90210', 'Seattle, WA'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Name: Chicago', result.output)
        self.assertIn('State: Illinois', result.output)
        self.assertIn('Name: Beverly Hills', result.output)
        self.assertIn('State: None', result.output)
        self.assertIn('Name: Seattle', result.output)
        self.assertIn('State: Washington', result.output)

    def test_valid_multiple_locations(self):
        result = self.runner.invoke(geoloc_util, ['Chicago, IL', '90210', 'Seattle, WA'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Name: Chicago', result.output)
        self.assertIn('State: Illinois', result.output)
        self.assertIn('Name: Beverly Hills', result.output)
        self.assertIn('State: None', result.output)
        self.assertIn('Name: Seattle', result.output)
        self.assertIn('State: Washington', result.output)

    def test_invalid_location(self):
        result = self.runner.invoke(geoloc_util, ['--locations', 'InvalidCity, XX'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('No results found for location: InvalidCity, XX', result.output)

    def test_empty_location(self):
        result = self.runner.invoke(geoloc_util, ['--locations', ''])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Empty location provided', result.output)

    def test_invalidCity_validState_location(self):
        result = self.runner.invoke(geoloc_util, ['--locations', 'InvalidCity, IL'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('No results found for location: InvalidCity, IL', result.output)

    def test_invalidZipCode(self):
        result = self.runner.invoke(geoloc_util, ['9999'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Error accessing API for ZIP code', result.output)

if __name__ == '__main__':
    unittest.main()