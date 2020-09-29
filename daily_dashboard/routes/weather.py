"""
https://www.weather.gov/documentation/services-web-api
"""

from flask import Blueprint, request, session, Response
from flask_login import login_required

bp = Blueprint('weather', __name__, url_prefix='/weather')