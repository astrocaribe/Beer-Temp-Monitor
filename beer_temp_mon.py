import time
import logging
from datetime import datetime as dt
import Adafruit_MCP9808.MCP9808 as MCP9808
import requests
import json
import sys

from helpers import utils

# ************************** LOGGING **************************
logger = logging.getLogger()

streamHandler = logging.StreamHandler()
fileHandler = logging.FileHandler('logs/b-monitor.log', mode='a')
formatter = logging.Formatter(
    '%(asctime)s %(name)-2s %(levelname)-5s %(message)s')
streamHandler.setFormatter(formatter)
fileHandler.setFormatter(formatter)

logger.addHandler(streamHandler)
logger.addHandler(fileHandler)
logger.setLevel(logging.INFO)

# ************************** CONFIGS **************************
with open('config/config.json') as jsonConfig:
    configData = json.load(jsonConfig)
    host = configData['service']['host']
    # port = configData['service']['port']
    route = configData['service']['route']

    slack_url = configData['slack']['slack_url']

    log_path = configData['logger']['path']
    log_when = configData['logger']['when']
    log_int = configData['logger']['interval']

# ************************** SENSOR INIT **************************
# Initialize the sensor
temp_sensor = MCP9808.MCP9808()
temp_sensor.begin()

# ************************** CONSTANTS **************************
location = [36.1388, -86.8426]  # Location
interval = 300  # Reading frequency, in seconds


# ************************** FUNCTIONS **************************

# # Convert celcius to fahrenheit
# def c_to_f(c):
#     return c * 9.0 / 5.0 + 32.0


def post_to_slack(url, msg):
    headers = {'Content-Type': 'application/json'}
    payload = {"text": msg}

    try:
        r = requests.post(url, headers=headers, data=json.dumps(payload))
        response_code = r.status_code

        if response_code == 503:
            logger.error('Slack may be unavailable. Please try again later!')
    except Exception as e:
        logger.error('Unspecified error.', e)
    else:
        logger.info('Slack message sent.')


# Retrieve local weather information
# def local_weather(loc):
#     key = "a7c0eba6c07ac8d3bc2f81535bcf8592"
#     url = "https://api.darksky.net/forecast/{0}/{1:.4f},{2:.4f}?exclude=[minutely,hourly,daily,alerts,flags]".format(
#         key, loc[0], loc[1])
#     headers = {'Content-Type': 'application/json'}

#     try:
#         resp = requests.get(url, headers=headers)
#     except Exception as e:
#         logger.error('Unspecified error. Please check DarkSky availability.', e)
#         local_temp = 0
#     else:
#         response_msg = json.loads(resp.text)
#         local_temp = response_msg['currently']['temperature']

#     return local_temp


def read_temp(loc):
    room_temp = temp_sensor.readTempC()
    weather_temp = utils.local_weather(loc, logger)
    # weather_temp = 65.09
    read_time = dt.utcnow().isoformat(' ')
    return room_temp, weather_temp, read_time


def post_temps(loc, time_int):
    # ToDo: Allow option to use port if neccesary
    # url = host + ':' + port + route
    url = host + route

    while True:
        r_temp, w_temp, r_time = read_temp(loc)
        payload = {"room": utils.c_to_f(r_temp), "weather": w_temp, "time": r_time}
        headers = {'Content-Type': 'application/json'}

        try:
            r = requests.post(url, headers=headers, data=json.dumps(payload))
        except requests.exceptions.ConnectionError:
            connection_msg = 'Connection refused. Please check that service is running.'
            post_to_slack(slack_url, connection_msg)
            logger.error(connection_msg, ' url: ', url)
            time.sleep(time_int)
        except Exception as e:
            unspecified_msg = 'Unspecified error. Please check the logs.'
            post_to_slack(slack_url, unspecified_msg)
            logger.error(unspecified_msg, e)
            sys.exit(0)
        except KeyboardInterrupt:
            logger.info('Ctrl-C detected. Shutting down ...')
            sys.exit(0)
        else:
            status = r.status_code

            if status == 200:
                response_msg = json.loads(r.text)
                logger.info(
                    'Room: {0:.3f}*F - Weather: {1:.3f}*F - Time: {2} - Status: {3}'.format(utils.c_to_f(r_temp), w_temp,
                                                                                            r_time,
                                                                                            response_msg['message']))
            elif status == 503:
                unavailable_msg = 'Service may be unavailable. Please check and try again shortly! Status: {}'.format(
                    status)
                post_to_slack(slack_url, unavailable_msg)
                logger.error(unavailable_msg)

            time.sleep(time_int)


def main(loc, time_int):
    post_to_slack(slack_url, "Beer Temperature Monitor has started!")
    print('Press Ctrl+C to quit.')

    # Read and post tempetatures to API evey time_int
    post_temps(loc, time_int)


if __name__ == "__main__":
    main(location, interval)
