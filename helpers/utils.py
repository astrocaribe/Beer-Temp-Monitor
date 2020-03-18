import requests
import json

# Convert celcius to fahrenheit
def c_to_f(c):
    return c * 9.0 / 5.0 + 32.0

# Retrieve local weather information
def local_weather(loc, logger):
    key = "a7c0eba6c07ac8d3bc2f81535bcf8592"
    url = "https://api.darksky.net/forecast/{0}/{1:.4f},{2:.4f}?exclude=[minutely,hourly,daily,alerts,flags]".format(
        key, loc[0], loc[1])
    headers = {'Content-Type': 'application/json'}

    try:
        resp = requests.get(url, headers=headers)
    except Exception as e:
        logger.error('Unspecified error. Please check DarkSky availability.', e)
        local_temp = 0
    else:
        response_msg = json.loads(resp.text)
        local_temp = response_msg['currently']['temperature']

    return local_temp