from flask import Blueprint, render_template, g
from flask_login import login_required, current_user

from daily_dashboard.dto.device_dto import DeviceDto
from daily_dashboard.helpers.credential_manager import use_credentials
from daily_dashboard.helpers.device_manager import use_device
from daily_dashboard.providers.google.calendars import get_calendar_list

bp = Blueprint('sessions', __name__, url_prefix='/sessions')


@bp.route('/', methods=('GET',))
@login_required
@use_credentials
@use_device
def active():
    calendar_list = get_calendar_list(g.credentials)
    device_dtos = [
        DeviceDto(device, is_current=(device.id == g.device.id), calendar_list=calendar_list)
        for device in current_user.devices
    ]

    return render_template('active_sessions.html', devices=device_dtos)
