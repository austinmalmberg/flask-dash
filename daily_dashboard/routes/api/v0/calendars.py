from datetime import datetime, timedelta
import pytz

from flask import Blueprint, request, jsonify, render_template, g
from flask_login import login_required

from daily_dashboard.dto.event_dto import EventDto
from daily_dashboard.helpers.credential_manager import use_credentials
from daily_dashboard.helpers.device_manager import use_device
from daily_dashboard.providers.google.calendars import get_events_from_multiple_calendars, get_colors
from daily_dashboard.util.dt_formatter import strftime_date_format, strftime_time_format

bp = Blueprint('calendar_api', __name__, url_prefix='/api/v0')


@bp.route('/events', methods=('GET',))
@login_required
@use_credentials
@use_device
def events():
    # session variable for max_days not implemented yet
    max_days = 7  # session.get('max_days', 7)

    timezone = pytz.timezone(g.device.timezone)

    try:
        # make sure the date arg is formatted correctly
        iso_date_str = request.args.get('date', None)
        locale_date = datetime.fromisoformat(iso_date_str).date()
    except (ValueError, TypeError):
        # fallback to date at timezone
        locale_date = datetime.now(timezone).date()

    dates = [locale_date + timedelta(days=i) for i in range(max_days)]

    event_list = get_events_from_multiple_calendars(
        g.credentials, g.device.watched_calendars,
        dt_min=locale_date,
        max_days=max_days,
        timezone=timezone
    )

    calendar_colors = get_colors(g.credentials)

    event_dtos = [EventDto(event, colors=calendar_colors) for event in event_list]

    platform = request.user_agent.platform
    date_format = strftime_date_format(g.device.date_order, platform)
    time_format = strftime_time_format(g.device.time_24hour, platform)

    if request.args.get('res', None) == 'json':
        return jsonify([dto.__dict__ for dto in event_dtos])

    return render_template(
        'components/events.html',
        dates=dates,
        date_format=date_format,
        time_format=time_format,
        events=event_dtos
    )
