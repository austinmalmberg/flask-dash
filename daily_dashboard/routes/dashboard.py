from datetime import datetime, timedelta
import pytz

from flask import Blueprint, render_template, session, redirect, url_for, request
from flask_login import login_required, current_user

from daily_dashboard.database import db
from daily_dashboard.database.queries import sync_calendars
from daily_dashboard.helpers.google import build_credentials
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
    locale_date = datetime.now(pytz.timezone(current_user.timezone)).date()
    dates = [locale_date + timedelta(days=i) for i in range(7)]

    return render_template('dashboard.html', dates=dates)


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

    return render_template('settings.html')


@bp.route('/login')
def login():
    if 'device_credentials' not in session or datetime.utcnow() > session['device_credentials']['valid_until']:
        session['device_credentials'] = oauth_limited_input_device.create_device_credentials()

    return render_template('login.html', device_credentials=session['device_credentials'])
