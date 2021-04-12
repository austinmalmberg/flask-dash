"""
TODO: Store weather in a Redis database
TODO: Return cached weather unless it older than X minutes
TODO: Allow user to update their location through `/settings`
TODO: Allow user to update their preferred weather units through `/settings`
"""

from flask import Blueprint, request, render_template, g
from flask_login import login_required

from daily_dashboard.helpers.location_manager import use_location
from daily_dashboard.providers.openweathermap import request_weather, ACCEPTABLE_UNITS
from daily_dashboard.dto.weather_dto import WeatherDto, CurrentWeatherDto
from daily_dashboard.util.errors import BaseApplicationException

bp = Blueprint('weather_api', __name__, url_prefix='/api/v0')


@bp.route('/weather', methods=('GET',))
@login_required
@use_location
def forecast():
    """
    Requests the weather through the OpenWeatherMap API with 'lat' and 'lon' variables set by the 'use_location'
    decorator.

    Possible error responses:
        400 - use_location aborted the request due to missing or invalid variables
        504 - There was an error requesting the weather from the provider
    """

    kwargs = dict()
    units = request.args.get('units', None)
    if units in ACCEPTABLE_UNITS:
        kwargs[units] = units

    try:
        weather = request_weather(g.lat, g.lon, **kwargs)
    except BaseApplicationException as err:
        return err.as_json()

    forecasts = weather['daily']
    weather_dtos = []

    for i, forecastObj in enumerate(forecasts):
        dto = CurrentWeatherDto(forecastObj, weather['current']) if i == 0 else WeatherDto(forecastObj)
        weather_dtos.append(dto)

    # res_type == 'template' so create weather dtos from weather data
    return render_template('components/forecast.html', weather_dtos=weather_dtos)
