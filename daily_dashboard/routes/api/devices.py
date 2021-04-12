
from flask import Blueprint, g, jsonify, request
from flask_login import login_required

from daily_dashboard.data_access.devices import set_device_position
from daily_dashboard.dto.device_dto import DeviceDto
from daily_dashboard.helpers.device_manager import use_device
from daily_dashboard.util.errors import BaseApplicationException

bp = Blueprint('device_api', __name__, url_prefix='/api/device')


@bp.route('/', methods=('GET', 'PUT'))
@login_required
@use_device
def current_device():
    if request.method == 'PUT':
        lat = request.json.get('lat', None)
        lon = request.json.get('lon', None)

        error = None
        if lat is None:
            error = "Missing parameter 'lat'"
        elif lon is None:
            error = "Missing parameter 'lon'"

        try:
            lat = float(lat)
            lon = float(lon)
        except (TypeError, ValueError):
            error = "'lat' and 'lon' parameters must be of type float"

        if error:
            return BaseApplicationException(
                status=400,
                title='Bad request',
                message=error
            ).as_json()

        set_device_position(g.device, lat, lon)

        return '', 200

    return jsonify(DeviceDto(g.device).__dict__)
