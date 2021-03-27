import os

import requests

from daily_dashboard.util.errors import BaseApplicationException

BASE_ENDPOINT = 'https://api.openweathermap.org/data/2.5/onecall'
EXCLUDE = ['minutely', 'hourly']
ACCEPTABLE_UNITS = ['imperial', 'metric', 'standard']


def request_weather(lat, lon, units='imperial'):

    params = {
        'lat': lat,
        'lon': lon,
        'units': units,
        'exclude': ','.join(EXCLUDE),
        'appid': os.environ['OWM_API_KEY']
    }

    response = requests.get(BASE_ENDPOINT, params=params)

    if response.status_code != 200:
        raise BaseApplicationException(
            status=504,
            title='Weather Service Error',
            message='There was a problem retrieving the weather for your location. Please try again later.'
        )

    return response.json()
