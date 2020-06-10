from datetime import datetime

from flask import Blueprint, render_template, session, redirect, url_for
from flask_login import login_required, current_user

from database.models import Calendar
from routes.google import oauth_limited_input_device
from routes.google.calendars import get_calendar_list
from routes.google.oauth import validate_oauth_token

bp = Blueprint('main', __name__)


@bp.route('/')
@login_required
def dashboard():
    """
    Sends basic template. Uses frontend AJAX calls to app endpoints that populate weather and events

    :return: The template
    """

    # get events for each calendar
    # start watching calendars

    # get weather

    return render_template('dashboard.html')


@bp.route('/settings', methods=('GET', 'POST'))
@validate_oauth_token
@login_required
def settings():
    """
    View and update user settings

    GET -- returns JSON representing user settings
    POST -- updates user settings

    :return:
    """
    calendars = get_calendar_list()

    for calendar in calendars:
        found = Calendar.query.filter_by(calendar_id=calendar.get('id', '')).first()
        if found:
            calendar['checked'] = True

    return render_template('settings.html', calendars=calendars)


@bp.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if 'device_credentials' not in session or datetime.utcnow() > session['device_credentials']['valid_until']:
        session['device_credentials'] = oauth_limited_input_device.create_device_credentials()

    return render_template('login.html', device_credentials=session['device_credentials'])
