import unittest
import json
from unittest.mock import patch
from helpers import utils

class TestTemperatureConversion(unittest.TestCase):

    def test_temperature_conversion(self):
        self.assertEqual(utils.c_to_f(0), 32)


class TestLocalWeather(unittest.TestCase):

    def test_local_weather_request(self):
        with patch('requests.get') as mock_get:
        
            # Configure the mock to return a response with an OK status code.
            mock_get.return_value.ok = True
            mock_get.return_value.text = json.dumps({"currently" : {"temperature" : 70.13}})

            # Call the service, which will send a request to the server.
            response = utils.local_weather([12, 12], 'sample')

            self.assertEqual(response, 70.13)

        # with patch('requests.get') as mock_get:
        #     with self.assertRaises(Exception) as context:
        
        #         # Configure the mock to return a response with an OK status code.
        #         mock_get.return_value.ok = True
        #         # mock_get.return_value.text = json.dumps(raise Exception('Some exception'))

        #         # Call the service, which will send a request to the server.
        #         response = utils.local_weather([12, 12], 'sample')

        #         self.assertTrue(response, context.exception)


if __name__ == '__main__':
    unittest.main()