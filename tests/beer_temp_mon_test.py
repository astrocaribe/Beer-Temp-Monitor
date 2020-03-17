from mock import MagicMock
import sys
import unittest
sys.path.append('./src/')

from beer_temp_mon import c_to_f, local_weather


def c_to_f_test():
    '''
    Given a temperature in Celcius, returns Fahrenheit.
    '''
    assert c_to_f(0) == 32

def local_weather_test():
    '''
    Given a location, requests weather fro such location.
    '''

    # requests.get = MagicMock(return_value={"currently": {"temperature": 0}})
    assert local_weather("someloc") == 32

if __name__ == '__main__':
    unittest.main()
