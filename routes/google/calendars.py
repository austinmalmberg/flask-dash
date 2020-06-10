from flask import Blueprint, jsonify
from flask_login import login_required


from helpers.google.calendars import get_calendar_list, get_calendar_settings
from routes.google.oauth import validate_oauth_token

bp = Blueprint('calendars', __name__, url_prefix='/calendars')


@bp.route('/list', methods=('GET',))
@validate_oauth_token
@login_required
def list_all():
    """
    Returns a list of all calendars for the user.
    :return:
    """
    calendars = get_calendar_list()

    return jsonify(calendars)


@bp.route('/upcoming_events', methods=('GET',))
@validate_oauth_token
@login_required
def upcoming_events():
    pass


@bp.route('/settings', methods=('GET',))
@validate_oauth_token
@login_required
def settings():
    settings = get_calendar_settings()

    return jsonify(settings)
