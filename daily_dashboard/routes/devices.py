from flask import Blueprint, render_template
from flask_login import login_required, current_user

from daily_dashboard.database.data_access.devices import update_device_uuids
from daily_dashboard.dto.device_dto import DeviceDto

bp = Blueprint('devices', __name__, url_prefix='/devices')


@bp.route('/', methods=('GET',))
@login_required
def list_devices():
    devices = current_user.devices
    update_device_uuids(devices)

    device_dtos = [DeviceDto(device) for device in devices]

    return render_template('devices.html', devices=device_dtos)
