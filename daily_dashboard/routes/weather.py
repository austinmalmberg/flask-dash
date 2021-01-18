"""
Prefix:     /weather
Endpoints:

/<lat:int>,<long:int>       Takes latitude/longitude and returns the current weather
    Options:
    - format [json, html]   Default json

TODO: Store weather in a Redis database
TODO: Return cached weather unless it older than X minutes
TODO: Allow user to update their location through `/settings`
TODO: Allow user to update their preferred weather units through `/settings`

"""

import os
import requests

from flask import Blueprint, request, session, jsonify, render_template
from flask_login import login_required, current_user

from daily_dashboard.dto.weather_dto import WeatherDto, CurrentWeatherDto
from daily_dashboard.util.errors import BaseError

bp = Blueprint('weather', __name__, url_prefix='/weather')

BASE_ENDPOINT = 'https://api.openweathermap.org/data/2.5/onecall'
EXCLUDE = ['minutely', 'hourly']
# ACCEPTABLE_UNITS = {'standard', 'imperial', 'metric'}


@bp.route('/<float_neg:lat>,<float_neg:lon>', methods=('GET',))
@login_required
def fetch(lat, lon):
    units = request.args.get('units', None)
    if units is None:
        if 'weather_units' not in session:
            session['weather_units'] = 'imperial' if current_user.locale == 'en' else 'metric'
        units = session['weather_units']

    params = {
        'lat': lat,
        'lon': lon,
        'exclude': ','.join(EXCLUDE),
        'units': units,
        'appid': os.environ['OWM_API_KEY']
    }

    response = requests.get(BASE_ENDPOINT, params=params)

    as_json_response = request.args.get('res', None) == 'json'

    if response.status_code != 200:
        error = BaseError(
            status=504,
            title='Weather Service Error',
            message='There was a problem retrieving the weather for your location. Please try again later.'
        )
        return (error.as_json() if as_json_response else error.as_template()), error.status

    data = response.json()
    if as_json_response:
        return jsonify(data)

    # only need 7 day forecast. This API returns 8
    forecasts = data['daily'][:7]
    weather_dtos = []

    for i, forecast in enumerate(forecasts):
        dto = CurrentWeatherDto(forecast, data['current']) if i == 0 else WeatherDto(forecast)
        weather_dtos.append(dto)

    return render_template('components/forecast.html', weather_dtos=weather_dtos)
