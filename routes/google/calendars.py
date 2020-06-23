from flask import Blueprint, jsonify
from flask_login import login_required, current_user

from helpers.google.calendars import get_calendar_list, get_calendar_settings, get_events_from_multiple_calendars,\
    get_colors
from routes.google.oauth import validate_oauth_token

bp = Blueprint('calendars', __name__, url_prefix='/calendars')


@bp.route('/list', methods=('GET',))
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
    credentials = current_user.build_credentials()
    watched_calendars = [cal.calendar_id for cal in current_user.calendars if cal.watching]

    events = get_events_from_multiple_calendars(credentials, watched_calendars, current_user.timezone)

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
