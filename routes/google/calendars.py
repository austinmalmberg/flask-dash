from datetime import date

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

from helpers.google.calendars import get_calendar_list, get_calendar_settings, get_events_from_multiple_calendars,\
    get_colors
from routes.google.oauth import validate_oauth_token

bp = Blueprint('calendars', __name__, url_prefix='/calendars')


@bp.route('/', methods=('GET',))
@login_required
@validate_oauth_token
def calendar_list():
    """
    Returns a list of all calendars for the user.
    :return:
    """
    credentials = current_user.build_credentials()
    calendars = get_calendar_list(credentials)

    return jsonify(calendars)


@bp.route('/events', methods=('GET',))
@login_required
@validate_oauth_token
def events():
    time_min = request.args.get('timeMin')
    time_range = request.args.get('range')

    error_msg = None

    if time_min:
        try:
            date_min = date.fromisoformat(time_min[:10])
        except ValueError:
            error_msg = 'timeMin must be a date in ISO format'
    else:
        error_msg = "Missing request parameter 'timeMin'"

    if time_range and error_msg is None:
        try:
            time_range = int(time_range)
            if time_range <= 0:
                error_msg = 'Range must be greater than 0'
        except ValueError:
            error_msg = 'Range must be a number, if present'

    if error_msg:
        return jsonify({
            'error': 'Invalid parameter',
            'message': error_msg
        }), 400

    if not time_range:
        time_range = 7

    credentials = current_user.build_credentials()
    watched_calendar_ids = [cal.calendar_id for cal in current_user.calendars if cal.watching]

    events = get_events_from_multiple_calendars(
        credentials, watched_calendar_ids,
        date_min=date_min,
        time_range=time_range
    )

    return jsonify(events)


@bp.route('/settings', methods=('GET',))
@login_required
@validate_oauth_token
def settings():
    credentials = current_user.build_credentials()
    settings = get_calendar_settings(credentials)

    return jsonify(settings)


@bp.route('/colors', methods=('GET',))
@login_required
@validate_oauth_token
def colors():
    credentials = current_user.build_credentials()
    colors = get_colors(credentials)

    return jsonify(colors)
