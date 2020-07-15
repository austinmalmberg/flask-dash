from datetime import datetime

from flask import Blueprint, jsonify, request, session
from flask_login import login_required, current_user

from daily_dashboard.helpers.google import build_credentials
from daily_dashboard.helpers.google.calendars import get_calendar_list, get_calendar_settings, get_events_from_multiple_calendars,\
    get_colors
from daily_dashboard.routes.google.oauth import validate_oauth_token

bp = Blueprint('calendars', __name__, url_prefix='/calendars')


@bp.route('/', methods=('GET',))
@login_required
@validate_oauth_token
def calendar_list():
    """
    Returns a list of all calendars for the user.
    :return:
    """
    credentials = build_credentials(token=session.get('token', None), refresh_token=current_user.refresh_token)
    calendars = get_calendar_list(credentials)

    return jsonify(calendars)


@bp.route('/events', methods=('GET',))
@login_required
@validate_oauth_token
def events():
    time_min = request.args.get('timeMin')
    max_days = request.args.get('maxDays')

    error_msg = None

    if time_min:
        try:
            time_min = time_min.replace('Z', '')
            date_min = datetime.fromisoformat(time_min)
        except ValueError:
            error_msg = 'timeMin must be a date in ISO format'
            print(time_min, error_msg)
    else:
        error_msg = "Missing request parameter 'timeMin'"

    if max_days and error_msg is None:
        try:
            max_days = int(max_days)
            if max_days <= 0:
                error_msg = 'maxDays must be greater than 0'
        except ValueError:
            error_msg = 'maxDays must be a number, if present'

    if error_msg:
        return jsonify({
            'error': 'Invalid parameter',
            'message': error_msg
        }), 400

    credentials = build_credentials(token=session.get('token', None), refresh_token=current_user.refresh_token)
    watched_calendar_ids = [cal.calendar_id for cal in current_user.calendars if cal.watching]

    events = get_events_from_multiple_calendars(
        credentials, watched_calendar_ids,
        date_min=date_min,
        max_days=max_days
    )

    return jsonify(events)


@bp.route('/settings', methods=('GET',))
@login_required
@validate_oauth_token
def settings():
    credentials = build_credentials(token=session.get('token', None), refresh_token=current_user.refresh_token)
    settings = get_calendar_settings(credentials)

    return jsonify(settings)


@bp.route('/colors', methods=('GET',))
@login_required
@validate_oauth_token
def colors():
    credentials = build_credentials(token=session.get('token', None), refresh_token=current_user.refresh_token)
    colors = get_colors(credentials)

    return jsonify(colors)
