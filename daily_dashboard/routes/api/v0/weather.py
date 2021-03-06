"""
TODO: Store weather in a Redis database
TODO: Return cached weather unless it older than X minutes
TODO: Allow user to update their location through `/settings`
TODO: Allow user to update their preferred weather units through `/settings`
"""

from flask import Blueprint, request, render_template, g
from flask_login import login_required

from daily_dashboard.helpers.device_manager import use_device
from daily_dashboard.providers.openweathermap import request_weather, ACCEPTABLE_UNITS
from daily_dashboard.dto.weather_dto import WeatherDto, CurrentWeatherDto
from daily_dashboard.util.errors import BaseApplicationException

bp = Blueprint('weather_api', __name__, url_prefix='/api/v0')


@bp.route('/weather', methods=('GET',))
@login_required
@use_device
def forecast():
    """
    Requests the weather through the OpenWeatherMap API

    Possible error responses:
        400 - Location not set on the device
        504 - There was an error requesting the weather from the provider
    """

    kwargs = dict()
    units = request.args.get('units', None)
    if units in ACCEPTABLE_UNITS:
        kwargs[units] = units

    if g.device.position is None:
        return BaseApplicationException(
            status=400,
            title='Bad request',
            message='Location not set. Share location or update in settings'
        ).as_json()

    try:
        lat, lon = g.device.position
        weather = request_weather(lat, lon, **kwargs)
    except BaseApplicationException as err:
        return err.as_json()

    forecasts = weather['daily']
    weather_dtos = []

    for i, forecastObj in enumerate(forecasts):
        dto = CurrentWeatherDto(forecastObj, weather['current']) if i == 0 else WeatherDto(forecastObj)
        weather_dtos.append(dto)

    # res_type == 'template' so create weather dtos from weather data
    return render_template('components/forecast.html', weather_dtos=weather_dtos)
