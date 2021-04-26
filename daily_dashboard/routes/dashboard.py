from datetime import datetime

from flask import Blueprint, render_template, session, redirect, url_for, request, g, abort
from flask_login import login_required, current_user

from daily_dashboard.data_access.devices import update_device_settings, get_device_by_uuid
from daily_dashboard.forms.settings import SettingsForm
from daily_dashboard.helpers.credential_manager import use_credentials
from daily_dashboard.helpers.device_manager import use_device
from daily_dashboard.providers.google.calendars import get_calendar_list
from daily_dashboard.routes.google import oauth_limited_input_device

bp = Blueprint('main', __name__)


@bp.route('/')
@login_required
@use_device
def dashboard():
    """
    Sends basic dashboard template.

    :return: The template
    """

    # session variable for max_days not implemented yet
    max_days = 7  # session.get('max_days', 7)

    date_order = ('date', 'month') if g.device.date_order == 'DMY' else ('month', 'date')

    return render_template(
        'dashboard.html',
        card_count=max_days,
        date_order=date_order,
        clock_24hr=g.device.time_24hour,
        external_login_endpoint=url_for('main.login', _external=True),
        position_set=g.device.position is not None
    )


@bp.route('/settings', methods=('GET', 'POST'))
@login_required
@use_credentials
@use_device
def settings():
    """
    View and update user settings

    GET -- returns JSON representing user settings
    POST -- updates user settings

    :return:
    """
    form = SettingsForm(request.form)

    calendar_list = get_calendar_list(g.credentials)

    form.calendars.choices = [
        (calendar['id'], calendar['summary'], (calendar['id'] in g.device.watched_calendars))
        for calendar in calendar_list
    ]

    if request.method == 'POST' and form.validate():
        device = g.device

        if 'device_uuid' in request.form:
            uuid = request.args.get('uuid', None)
            device = get_device_by_uuid(uuid)
            if device is None:
                return abort(404)

        update_device_settings(
            device,
            name=form.device_name.data,
            date_order=form.date_format.data,
            time_24hour=form.time_format.data == '24hr',
            calendars=form.calendars.data,
            position=dict(lat=form.lat.data, lon=form.lon.data)
        )

        return redirect(url_for('index'))

    device = g.device
    if 'uuid' in request.args:
        uuid = request.args.get('uuid', None)
        device = get_device_by_uuid(uuid)
        if device is None:
            return abort(404)
        elif device.user_id != current_user.id:
            return abort(403)

    # prefill location info
    if device.position is not None:
        lat, lon = device.position
        if lat:
            form.lat.data = lat
        if lon:
            form.lon.data = lon

    form.device_uuid.data = device.uuid

    if g.device.name:
        form.device_name.data = device.name

    # set the selected date_format value
    form.date_format.data = device.date_order

    # set the selected time_format value
    form.time_format.data = '24hr' if device.time_24hour else '12hr'

    return render_template(
        'settings.html',
        form=form,
        current_device=(g.device.id == device.id)
    )


@bp.route('/login')
def login():
    if 'device_credentials' not in session or datetime.utcnow() > session['device_credentials']['valid_until']:
        session['device_credentials'] = oauth_limited_input_device.create_device_credentials()

    return render_template('login.html', device_credentials=session['device_credentials'])
