from flask import Blueprint, jsonify
from flask_login import login_required, current_user


from helpers.google.calendars import get_calendar_list, get_calendar_settings
from routes.google.oauth import validate_oauth_token

bp = Blueprint('calendars', __name__, url_prefix='/calendars')


@bp.route('/list', methods=('GET',))
@login_required
@validate_oauth_token
def list_all():
    """
    Returns a list of all calendars for the user.
    :return:
    """
    credentials = current_user.build_credentials()
    calendars = get_calendar_list(credentials)

    return jsonify(calendars)


@bp.route('/upcoming_events', methods=('GET',))
@login_required
@validate_oauth_token
def upcoming_events():
    pass


@bp.route('/settings', methods=('GET',))
@login_required
@validate_oauth_token
def settings():
    credentials = current_user.build_credentials()
    settings = get_calendar_settings(credentials)

    return jsonify(settings)
