"""
https://www.weather.gov/documentation/services-web-api
"""

from flask import Blueprint, request, session, Response
from flask_login import login_required

bp = Blueprint('weather', __name__, url_prefix='/weather')


@bp.route('/set', methods=('POST',))
@login_required
def set_data():

    if 'gridId' in request.args and 'gridX' in request.args and 'gridY' in request.args:
        session['grid_data'] = dict(
            gridId=request.args['gridId'],
            gridX=request.args['gridX'],
            gridY=request.args['gridY']
        )

    return Response(status=200)


@bp.route('/clear', methods=('POST',))
@login_required
def clear_data():
    session.pop('grid_data')

    return Response(status=200)


