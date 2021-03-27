from datetime import datetime, timedelta
import pytz

from flask import Blueprint, session, request, jsonify, render_template
from flask_login import login_required, current_user

from daily_dashboard.dto.event_dto import EventDto
from daily_dashboard.helpers.location_manager import use_location
from daily_dashboard.providers.google import build_credentials
from daily_dashboard.providers.google.calendars import get_events_from_multiple_calendars, get_colors
from daily_dashboard.util.dt_formatter import strftime_date_format, strftime_time_format

bp = Blueprint('calendar', __name__)


@bp.route('/events', methods=('GET',))
@login_required
@use_location
def events():
    # session variable for max_days not implemented yet
    max_days = session.get('max_days', 7)

    timezone = request.args.get('tz', None) or session.get('timezone', None) or current_user.timezone

    if 'watched_calendars' not in session:
        session['watched_calendars'] = [current_user.email]

    locale_date = datetime.now(pytz.timezone(timezone)).date()
    dates = [locale_date + timedelta(days=i) for i in range(max_days)]

    locale_date = datetime.now(pytz.timezone(timezone)).date()

    credentials = build_credentials(token=session.get('token', None), refresh_token=current_user.refresh_token)
    event_list = get_events_from_multiple_calendars(
        credentials, session['watched_calendars'],
        dt_min=locale_date,
        max_days=max_days,
        timezone=timezone
    )

    calendar_colors = get_colors(credentials)

    event_dtos = [EventDto(event, colors=calendar_colors) for event in event_list]

    platform = request.user_agent.platform
    date_format = strftime_date_format(session.get('dt_format', current_user.date_field_order), platform)
    time_format = strftime_time_format(session.get('clock_24hr', current_user.time_24hour), platform)

    if request.args.get('res', None) == 'json':
        return jsonify([dto.__dict__ for dto in event_dtos])

    return render_template(
        'components/events.html',
        dates=dates,
        date_format=date_format,
        time_format=time_format,
        events=event_dtos
    )
