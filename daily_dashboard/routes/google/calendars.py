from dateutil import parser
from flask import Blueprint, jsonify, request, session, render_template
from flask_login import login_required, current_user

from daily_dashboard.dto.event_dto import EventDto
from daily_dashboard.helpers.google import build_credentials
from daily_dashboard.helpers.google.calendars import get_calendar_list, get_calendar_settings, \
    get_events_from_multiple_calendars, get_colors
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


@bp.route('/events', methods=('GET',))
@login_required
@validate_oauth_token
@handle_refresh_error
def events():
    time_min = request.args.get('timeMin')
    max_days = request.args.get('maxDays')

    error = None

    # error if the request does not have a timeMin query param
    if not time_min:
        error = "Missing request parameter 'timeMin'"

    # attempt to convert the maxDays query param to an integer
    elif max_days:
        try:
            max_days = int(max_days)
            if max_days < 1:
                error = "'maxDays' must be greater than 0"
        except ValueError:
            error = "'maxDays' must be a number"

    try:
        dt_min = parser.isoparse(time_min)
    except ValueError:
        error = "'timeMin' must be a date in ISO format"

    if error:
        return jsonify({
            'error': 'Invalid parameter',
            'message': error
        }), 400

    credentials = build_credentials(session.get('token', None), current_user.refresh_token)
    watched_calendar_ids = [cal.calendar_id for cal in current_user.calendars if cal.watching]

    event_list = get_events_from_multiple_calendars(
        credentials, watched_calendar_ids,
        dt_min=dt_min,
        max_days=max_days
    )

    calendar_colors = get_colors(credentials)

    event_dtos = []
    for event in event_list:
        event_dtos.append(EventDto(event, colors=calendar_colors))

    return jsonify(events=event_dtos)


@bp.route('/events/<datetime:dt_min>', methods=('GET',))
@login_required
@validate_oauth_token
@handle_refresh_error
def events_from_date(dt_min):
    """
    Returns a list of events wrapped in a div.

    Optional query params:
        maxDays: An integer value. Default 7. Max 31.
        tz: A pytz timezone string. The timezone for the current_user is collected after authorization and stored in
            the database. It is also stored as a session variable when settings are changed. Passing a timezone as a
            query param will set this session variable; however, it will not be overridden if already set.
            Here is the priority in which it is used:
                1. query param (sets session variable, but does not override)
                2. session variable (set after authorization. can be changed in settings)
                3. database (set from user's calendar settings after authorization)

    :param dt_min: a datetime object set by util.converters.DateConverter. Looks for the pattern YYYY-mm-dd
    :return:
    """
    error = None

    max_days = request.args.get('maxDays')

    # attempt to convert the maxDays query param to an integer
    if max_days:
        try:
            max_days = int(max_days)
            if max_days < 1:
                error = 'maxDays must be greater than 0'
        except ValueError:
            error = "'maxDays' must be a number"

    timezone = request.args.get('tz')
    if not timezone:
        timezone = session.get('timezone', current_user.timezone)
    elif 'timezone' not in session:
        session['timezone'] = timezone

    if error:
        return jsonify({
            'error': 'Invalid parameter',
            'message': error
        }), 400

    credentials = build_credentials(session.get('token', None), current_user.refresh_token)
    watched_calendar_ids = [cal.calendar_id for cal in current_user.calendars if cal.watching]

    event_list = get_events_from_multiple_calendars(
        credentials, watched_calendar_ids,
        dt_min=dt_min,
        max_days=max_days,
        timezone=timezone
    )

    calendar_colors = get_colors(credentials)

    event_dtos = []
    for event in event_list:
        event_dtos.append(event_dto(event, calendar_colors))

    return render_template('components/events.html', events=event_dtos, platform=request.user_agent.platform)


@bp.route('/settings', methods=('GET',))
@login_required
@validate_oauth_token
@handle_refresh_error
def settings():
    credentials = build_credentials(session.get('token', None), current_user.refresh_token)

    return jsonify(get_calendar_settings(credentials))


@bp.route('/colors', methods=('GET',))
@login_required
@validate_oauth_token
@handle_refresh_error
def colors():
    credentials = build_credentials(session.get('token', None), current_user.refresh_token)

    return jsonify(get_colors(credentials))
