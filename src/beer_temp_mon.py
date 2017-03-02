import time
from datetime import datetime as dt
import Adafruit_MCP9808.MCP9808 as MCP9808
import urllib2
import json


# Convert celcius to fahrenheit
def c_to_f(c):
    return c * 9.0 / 5.0 + 32.0


# Initialize the sensor
temp_sensor = MCP9808.MCP9808()
temp_sensor.begin()


# Return external service url/port
def returnHost():
    with open('config/config.json') as jsonConfig:
        configData = json.load(jsonConfig)

    return configData['service']['host'] + ':' + configData['service']['port'] + configData['service']['route']


# Retrieve local weather information
def local_weather(loc):
    key = "a7c0eba6c07ac8d3bc2f81535bcf8592"
    url = "https://api.darksky.net/forecast/{0}/{1:.4f},{2:.4f}?exclude=[minutely,hourly,daily,alerts,flags]".format(key, loc[0], loc[1])

    f = urllib2.urlopen(url)
    json_string = f.read()
    parsed_json = json.loads(json_string)
    local_temp = parsed_json['currently']['temperature']

    return local_temp


def read_temp(loc):

    room_temp = temp_sensor.readTempC()
    weather_temp = 65.00        # TEMPORARY!!!
    # weather_temp = local_weather(loc)
    read_time = dt.utcnow()

    return room_temp, weather_temp, read_time


def post_temp(loc):

    url = returnHost()
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')

    while True:
        r_temp, w_temp, r_time = read_temp(loc)
        res = urllib2.urlopen(req, json.dumps([c_to_f(r_temp), w_temp]))
        status = res.read()

        print('Room: {0:.3f}*F - Weather: {1:.3f}*F - Time: {2} - Status: {3}'.format(c_to_f(r_temp), w_temp, r_time, 'Ok!'))

        time.sleep(interval)


# ------------- Main -------------
# Loop printing measurements every x minutes
location = [36.1388, -86.8426]    # Location
interval = 10                    # Rerading frequency, in seconds

print('Press Ctrl+C to quit.')
post_temp(location)
