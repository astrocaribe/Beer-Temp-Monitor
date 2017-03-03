import time
from datetime import datetime as dt
import Adafruit_MCP9808.MCP9808 as MCP9808
import requests
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
    headers = {'Content-Type': 'application/json'}

    try:
        resp = requests.get(url, headers=headers)

    except Exception:
        print('Unspecified error. Please check DarkSky availability.')
        local_temp = 0
    else:
        response_msg = json.loads(resp.text)
        local_temp = response_msg['currently']['temperature']

    return local_temp


def read_temp(loc):

    room_temp = temp_sensor.readTempC()
    weather_temp = local_weather(loc)
    # weather_temp = 65.09
    read_time = dt.utcnow()

    return room_temp, weather_temp, read_time


def post_temp(loc):

    url = returnHost()

    while True:
        r_temp, w_temp, r_time = read_temp(loc)
        payload = {"room": c_to_f(r_temp), "weather": w_temp}
        headers = {'Content-Type': 'application/json'}

        try:
            r = requests.post(url, headers=headers, data=json.dumps(payload))
        except requests.exceptions.ConnectionError:
            print('Connection refused. Please check that service is running.')
            return False
        except Exception:
            print('Unspecified error.')
            return False
        else:
            response_msg = json.loads(r.text)

            print('Room: {0:.3f}*F - Weather: {1:.3f}*F - Time: {2} - Status: {3}'.format(c_to_f(r_temp), w_temp, r_time, response_msg['message']))
            time.sleep(interval)


# ------------- Main -------------
# Loop printing measurements every x minutes
location = [36.1388, -86.8426]    # Location
interval = 300                    # Rerading frequency, in seconds

print('Press Ctrl+C to quit.')
post_temp(location)
