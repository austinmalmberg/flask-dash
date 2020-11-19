"""
https://www.weather.gov/documentation/services-web-api
"""

from flask import Blueprint

bp = Blueprint('weather', __name__, url_prefix='/weather')
