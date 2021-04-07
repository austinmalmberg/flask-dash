"""
TODO: Store weather in a Redis database
TODO: Return cached weather unless it older than X minutes
TODO: Allow user to update their location through `/settings`
TODO: Allow user to update their preferred weather units through `/settings`
"""

from flask import Blueprint, request, jsonify, render_template, g
from flask_login import login_required

from daily_dashboard.helpers.request_context_manager import use_location
from daily_dashboard.providers.openweathermap import request_weather, ACCEPTABLE_UNITS
from daily_dashboard.dto.weather_dto import WeatherDto, CurrentWeatherDto
from daily_dashboard.util.errors import BaseApplicationException

bp = Blueprint('weather_api', __name__, url_prefix='/api/v0')


@bp.route('/weather', methods=('GET',))
@login_required
@use_location
def forecast():
    """
    Use args 'lat' and 'lon' to request weather. If not provided, use IP address to get location

    Error responses:
        400 - 'lat' and 'lon' parameters were not float values
        412 - There was an error getting location from IP address and no lat/lon params were provided
        504 - There was an error requesting the weather from the provider
    """
    lat = request.args.get('lat', None)
    lon = request.args.get('lon', None)

    # check that lat and lon params are present and float values
    if lat and lon:
        try:
            g.lat = float(lat)
            g.lon = float(lon)
        except TypeError:
            return jsonify({
                'message': "Provide 'lat' and 'lon' params as float values"
            }), 400
    elif g.location_error:
        return jsonify({
            'message': f"{g.location_error}. Provide 'lat' and 'lon' params as float values"
        }), 412

    kwargs = dict()
    units = request.args.get('units', None)
    if units and units in ACCEPTABLE_UNITS:
        kwargs[units] = units

    try:
        weather = request_weather(g.lat, g.lon, **kwargs)
    except BaseApplicationException as err:
        return err.as_json(), err.status

    forecasts = weather['daily']
    weather_dtos = []

    for i, forecastObj in enumerate(forecasts):
        dto = CurrentWeatherDto(forecastObj, weather['current']) if i == 0 else WeatherDto(forecastObj)
        weather_dtos.append(dto)

    # res_type == 'template' so create weather dtos from weather data
    return render_template('components/forecast.html', weather_dtos=weather_dtos)
