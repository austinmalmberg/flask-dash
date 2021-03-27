from datetime import datetime, timedelta

import pytz
from flask import Blueprint, render_template, session, redirect, url_for, request
from flask_login import login_required, current_user

from daily_dashboard.forms.settings import SettingsForm
from daily_dashboard.helpers.location_manager import use_location
from daily_dashboard.providers.google import build_credentials
from daily_dashboard.providers.google.calendars import get_calendar_list
from daily_dashboard.routes.google import oauth_limited_input_device
from daily_dashboard.routes.google.oauth import validate_oauth_token, handle_refresh_error
from daily_dashboard.util.dt_formatter import strftime_date_format, strftime_time_format

bp = Blueprint('main', __name__)


@bp.route('/')
@login_required
@validate_oauth_token
@handle_refresh_error
@use_location
def dashboard():
    """
    Sends basic dashboard template.

    :return: The template
    """

    # session variable for max_days not implemented yet
    max_days = session.get('max_days', 7)

    timezone = request.args.get('tz', None) or session.get('timezone', None) or current_user.timezone

    if 'watched_calendars' not in session:
        session['watched_calendars'] = [current_user.email]

    locale_date = datetime.now(pytz.timezone(timezone)).date()
    dates = [locale_date + timedelta(days=i) for i in range(max_days)]

    platform = request.user_agent.platform
    date_format = strftime_date_format(session.get('dt_format', current_user.date_field_order), platform)
    time_format = strftime_time_format(session.get('clock_24hr', current_user.time_24hour), platform)

    return render_template(
        'dashboard.html',
        dates=dates,
        date_format=date_format,
        time_format=time_format,
        clock_24hr=session.get('clock_24hr', current_user.time_24hour)
    )


@bp.route('/settings', methods=('GET', 'POST'))
@login_required
@validate_oauth_token
@handle_refresh_error
@use_location
def settings():
    """
    View and update user settings

    GET -- returns JSON representing user settings
    POST -- updates user settings

    :return:
    """
    form = SettingsForm(request.form)
    form.zip_code.data = session['zip_code']

    calendar_list = get_calendar_list(
        build_credentials(token=session.get('token', None), refresh_token=current_user.refresh_token)
    )

    form.calendars.choices = [
        (calendar['id'], calendar['summary'], calendar['id'] in session.get('watched_calendars', []))
        for calendar in calendar_list
    ]

    if request.method == 'POST' and form.validate():
        session['watched_calendars'] = form.calendars.data
        session['dt_format'] = form.date_format.data
        session['clock_24hr'] = (form.time_format.data == '24hr')

        return redirect(url_for('main.dashboard'))

    # set the selected date_format value
    form.date_format.data = session.get('dt_format', current_user.date_field_order)

    # set the selected time_format value
    clock_24hr = session.get('clock_24hr', current_user.time_24hour)
    form.time_format.data = '24hr' if clock_24hr else '12hr'

    return render_template('settings.html', form=form)


@bp.route('/login')
def login():
    if 'device_credentials' not in session or datetime.utcnow() > session['device_credentials']['valid_until']:
        session['device_credentials'] = oauth_limited_input_device.create_device_credentials()

    return render_template('login.html', device_credentials=session['device_credentials'])
