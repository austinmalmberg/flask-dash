from flask import Blueprint
from flask_login import current_user, login_required

from googleapiclient.discovery import build

from routes.google.oauth import validate_oauth_token

bp = Blueprint('calendars', __name__, url_prefix='/calendars')

# Documentation -- https://developers.google.com/calendar/v3/reference/calendarList/list
calendar_list_url = 'https://www.googleapis.com/calendar/v3/users/me/calendarList'

# Documentation -- https://developers.google.com/calendar/v3/reference/colors/get
calendar_colors_url = 'https://www.googleapis.com/calendar/v3/colors'

# Documentation -- https://developers.google.com/calendar/v3/reference/settings/list
calendar_settings_url = 'https://www.googleapis.com/calendar/v3/users/me/settings'


# Documentation -- https://developers.google.com/calendar/v3/reference/events/list
def get_calendar_events_url(calendar_id):
    return f'https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events'


# Documentation -- https://developers.google.com/calendar/v3/reference/events/watch
def get_calendar_watch_url(calendar_id):
    return f'https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events/watch'


def get_service():
    return build('calendar', 'v3', credentials=current_user.credentials)


@bp.route('/list', methods=('GET',))
@login_required
@validate_oauth_token
def list_all():
    """
    Returns a list of all calendars for the user.
    :return:
    """
    service = get_service()


@bp.route('/upcoming_events', methods=('GET',))
@login_required
@validate_oauth_token
def upcoming_events():
    service = get_service()


@bp.route('/settings', methods=('GET',))
@login_required
@validate_oauth_token
def settings():
    service = get_service()
