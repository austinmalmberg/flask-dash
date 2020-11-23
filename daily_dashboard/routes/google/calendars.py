from flask import Blueprint, jsonify, session
from flask_login import login_required, current_user

from daily_dashboard.helpers.google import build_credentials
from daily_dashboard.helpers.google.calendars import get_calendar_list
from daily_dashboard.routes.google.oauth import validate_oauth_token, handle_refresh_error

bp = Blueprint('calendars', __name__, url_prefix='/calendars')


@bp.route('/', methods=('GET',))
@login_required
@validate_oauth_token
@handle_refresh_error
def calendar_list():
    """
    Returns a list of all calendars for the user.
    :return:
    """
    credentials = build_credentials(session.get('token', None), current_user.refresh_token)
    calendars = get_calendar_list(credentials)

    return jsonify(calendars)
