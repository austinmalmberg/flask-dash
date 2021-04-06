"""
TODO: Store weather in a Redis database
TODO: Return cached weather unless it older than X minutes
TODO: Allow user to update their location through `/settings`
TODO: Allow user to update their preferred weather units through `/settings`
"""

from flask import Blueprint, request, session, jsonify, render_template, flash, g
from flask_login import login_required

from daily_dashboard.helpers.request_context_manager import use_location
from daily_dashboard.providers.openweathermap import request_weather, ACCEPTABLE_UNITS
from daily_dashboard.dto.weather_dto import WeatherDto, CurrentWeatherDto
from daily_dashboard.util.errors import BaseApplicationException

bp = Blueprint('weather', __name__, url_prefix='/weather')


@bp.route('/', methods=('GET',))
@login_required
@use_location
def forecast():
    json_response = request.args.get('res', None) == 'json'

    kwargs = dict()
    units = request.args.get('units', None)
    if units and units in ACCEPTABLE_UNITS:
        kwargs['units'] = units
    elif 'weather_units' in session:
        kwargs['units'] = session['weather_units']

    try:
        weather = request_weather(g.location['lat'], g.location['lon'], **kwargs)
    except BaseApplicationException as err:
        flash(err.message)

        return (err.as_json() if json_response else err.as_template()), err.status

    forecasts = weather['daily']
    weather_dtos = []

    for i, forecastObj in enumerate(forecasts):
        dto = CurrentWeatherDto(forecastObj, weather['current']) if i == 0 else WeatherDto(forecastObj)
        weather_dtos.append(dto)

    if json_response:
        return jsonify([dto.__dict__ for dto in weather_dtos])

    # res_type == 'template' so create weather dtos from weather data
    return render_template('components/forecast.html', weather_dtos=weather_dtos)


@bp.route('/<float_neg:lat>,<float_neg:lon>', methods=('GET',))
@login_required
def forecast_from_coords(lat, lon):
    json_response = request.args.get('res', None) == 'json'

    kwargs = dict()
    units = request.args.get('units', None)
    if units and units in ACCEPTABLE_UNITS:
        kwargs['units'] = units
    elif 'weather_units' in session:
        kwargs['units'] = session['weather_units']

    try:
        weather = request_weather(lat, lon, **kwargs)
    except BaseApplicationException as err:
        flash(err.message)

        return (err.as_json() if json_response else err.as_template()), err.status

    forecasts = weather['daily']
    weather_dtos = []

    for i, forecast in enumerate(forecasts):
        dto = CurrentWeatherDto(forecast, weather['current']) if i == 0 else WeatherDto(forecast)
        weather_dtos.append(dto)

    if json_response:
        return jsonify([dto.__dict__ for dto in weather_dtos])

    # res_type == 'template' so create weather dtos from weather data
    return render_template('components/forecast.html', weather_dtos=weather_dtos)
