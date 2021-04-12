from flask import Blueprint, jsonify
from flask_login import login_required, current_user

from daily_dashboard.dto.device_dto import DeviceDto
from daily_dashboard.dto.user_dto import UserDto

bp = Blueprint('user_api', __name__, url_prefix='/api/user')


@bp.route('/')
@login_required
def me():
    return jsonify(UserDto(current_user).__dict__)


@bp.route('/devices')
@login_required
def all_devices():
    device_dtos = [DeviceDto(device) for device in current_user.devices]

    return jsonify([device.__dict__ for device in device_dtos])
