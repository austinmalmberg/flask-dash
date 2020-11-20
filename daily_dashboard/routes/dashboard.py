from datetime import datetime, timedelta

import pytz
from flask import Blueprint, render_template, session, redirect, url_for, request
from flask_login import login_required, current_user

from daily_dashboard.database import db
from daily_dashboard.database.queries import sync_calendars
from daily_dashboard.dto.event_dto import EventDto
from daily_dashboard.helpers.google import build_credentials
from daily_dashboard.helpers.google.calendars import get_events_from_multiple_calendars, get_colors
from daily_dashboard.routes.google import oauth_limited_input_device
from daily_dashboard.routes.google.calendars import get_calendar_list
from daily_dashboard.routes.google.oauth import validate_oauth_token, handle_refresh_error

bp = Blueprint('main', __name__)


@bp.route('/')
@login_required
@validate_oauth_token
@handle_refresh_error
def dashboard():
    """
    Sends basic dashboard template.

    :return: The template
    """
    # session variable for max_days not implemented yet
    max_days = session.get('max_days', 7)

    timezone = request.args.get('tz')
    if not timezone:
        timezone = session.get('timezone', current_user.timezone)

    locale_date = datetime.now(pytz.timezone(timezone)).date()
    dates = [locale_date + timedelta(days=i) for i in range(max_days)]

    credentials = build_credentials(session.get('token', None), current_user.refresh_token)
    watched_calendar_ids = [cal.calendar_id for cal in current_user.calendars if cal.watching]

    event_list = get_events_from_multiple_calendars(
        credentials, watched_calendar_ids,
        dt_min=locale_date,
        max_days=max_days,
        timezone=timezone
    )

    calendar_colors = get_colors(credentials)

    event_dtos = []
    for event in event_list:
        event_dtos.append(EventDto(event, colors=calendar_colors))

    return render_template('dashboard.html', dates=dates, events=event_dtos, platform=request.user_agent.platform)


@bp.route('/settings', methods=('GET', 'POST'))
@login_required
@validate_oauth_token
@handle_refresh_error
def settings():
    """
    View and update user settings

    GET -- returns JSON representing user settings
    POST -- updates user settings

    :return:
    """
    if request.method == 'POST':
        checked_ids = set(request.form.getlist('calendar'))

        for calendar in current_user.calendars:
            # begin watching checked calendars and stop watching unchecked calendars
            calendar.watching = str(calendar.id) in checked_ids

        db.session.commit()

        return redirect(url_for('main.dashboard'))

    # get an updated calendar list from Google
    credentials = build_credentials(token=session.get('token', None), refresh_token=current_user.refresh_token)
    google_calendars = get_calendar_list(credentials)

    sync_calendars(current_user, google_calendars)

    return render_template('settings.html', user_calendars=current_user.calendars)


@bp.route('/login')
def login():
    if 'device_credentials' not in session or datetime.utcnow() > session['device_credentials']['valid_until']:
        session['device_credentials'] = oauth_limited_input_device.create_device_credentials()

    return render_template('login.html', device_credentials=session['device_credentials'])
